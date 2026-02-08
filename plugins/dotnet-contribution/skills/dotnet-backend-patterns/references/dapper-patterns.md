# Dapper 模式和最佳实践

在 .NET 中使用 Dapper 进行高性能数据访问的高级模式。

## 为什么选择 Dapper？

| 方面            | Dapper                          | EF Core                |
| --------------- | ------------------------------- | ---------------------- |
| 性能            | 简单查询快约 10 倍              | 优化后性能良好         |
| 控制            | 完全 SQL 控制                   | 抽象化                 |
| 学习曲线        | 低（只需 SQL）                  | 较高                   |
| 复杂映射        | 手动                            | 自动                   |
| 更改跟踪        | 无                              | 内置                   |
| 迁移            | 外部工具                        | 内置                   |

**使用 Dapper 的场景：**

- 性能至关重要（热路径）
- 需要复杂 SQL（CTE、窗口函数）
- 读取密集型工作负载
- 遗留数据库架构

**使用 EF Core 的场景：**

- 具有关系的富领域模型
- 需要更改跟踪
- 需要 LINQ-to-SQL 转换
- 复杂对象图

## 连接管理

### 1. 正确的连接处理

```csharp
// 注册连接工厂
services.AddScoped<IDbConnection>(sp =>
{
    var connectionString = sp.GetRequiredService<IConfiguration>()
        .GetConnectionString("Default");
    return new SqlConnection(connectionString);
});

// 或使用工厂进行更多控制
public interface IDbConnectionFactory
{
    IDbConnection CreateConnection();
}

public class SqlConnectionFactory : IDbConnectionFactory
{
    private readonly string _connectionString;

    public SqlConnectionFactory(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("Default")
            ?? throw new InvalidOperationException("未找到连接字符串");
    }

    public IDbConnection CreateConnection() => new SqlConnection(_connectionString);
}
```

### 2. 连接生命周期

```csharp
public class ProductRepository
{
    private readonly IDbConnectionFactory _factory;

    public ProductRepository(IDbConnectionFactory factory)
    {
        _factory = factory;
    }

    public async Task<Product?> GetByIdAsync(string id, CancellationToken ct)
    {
        // 连接自动打开，在释放时关闭
        using var connection = _factory.CreateConnection();

        return await connection.QueryFirstOrDefaultAsync<Product>(
            new CommandDefinition(
                "SELECT * FROM Products WHERE Id = @Id",
                new { Id = id },
                cancellationToken: ct));
    }
}
```

## 查询模式

### 3. 基本 CRUD 操作

```csharp
// SELECT 单个
var product = await connection.QueryFirstOrDefaultAsync<Product>(
    "SELECT * FROM Products WHERE Id = @Id",
    new { Id = id });

// SELECT 多个
var products = await connection.QueryAsync<Product>(
    "SELECT * FROM Products WHERE CategoryId = @CategoryId",
    new { CategoryId = categoryId });

// INSERT 返回标识
var newId = await connection.QuerySingleAsync<int>(
    """
    INSERT INTO Products (Name, Price, CategoryId)
    VALUES (@Name, @Price, @CategoryId);
    SELECT CAST(SCOPE_IDENTITY() AS INT);
    """,
    product);

// INSERT 使用 OUTPUT 子句（返回完整实体）
var inserted = await connection.QuerySingleAsync<Product>(
    """
    INSERT INTO Products (Name, Price, CategoryId)
    OUTPUT INSERTED.*
    VALUES (@Name, @Price, @CategoryId);
    """,
    product);

// UPDATE
var rowsAffected = await connection.ExecuteAsync(
    """
    UPDATE Products
    SET Name = @Name, Price = @Price, UpdatedAt = @UpdatedAt
    WHERE Id = @Id
    """,
    new { product.Id, product.Name, product.Price, UpdatedAt = DateTime.UtcNow });

// DELETE
await connection.ExecuteAsync(
    "DELETE FROM Products WHERE Id = @Id",
    new { Id = id });
```

### 4. 动态查询构建

```csharp
public async Task<IReadOnlyList<Product>> SearchAsync(ProductSearchCriteria criteria)
{
    var sql = new StringBuilder("SELECT * FROM Products WHERE 1=1");
    var parameters = new DynamicParameters();

    if (!string.IsNullOrWhiteSpace(criteria.SearchTerm))
    {
        sql.Append(" AND (Name LIKE @SearchTerm OR Sku LIKE @SearchTerm)");
        parameters.Add("SearchTerm", $"%{criteria.SearchTerm}%");
    }

    if (criteria.CategoryId.HasValue)
    {
        sql.Append(" AND CategoryId = @CategoryId");
        parameters.Add("CategoryId", criteria.CategoryId.Value);
    }

    if (criteria.MinPrice.HasValue)
    {
        sql.Append(" AND Price >= @MinPrice");
        parameters.Add("MinPrice", criteria.MinPrice.Value);
    }

    if (criteria.MaxPrice.HasValue)
    {
        sql.Append(" AND Price <= @MaxPrice");
        parameters.Add("MaxPrice", criteria.MaxPrice.Value);
    }

    // 分页
    sql.Append(" ORDER BY Name");
    sql.Append(" OFFSET @Offset ROWS FETCH NEXT @PageSize ROWS ONLY");
    parameters.Add("Offset", (criteria.Page - 1) * criteria.PageSize);
    parameters.Add("PageSize", criteria.PageSize);

    using var connection = _factory.CreateConnection();
    var results = await connection.QueryAsync<Product>(sql.ToString(), parameters);
    return results.ToList();
}
```

### 5. 多映射（联接）

```csharp
// 一对一映射
public async Task<Product?> GetProductWithCategoryAsync(string id)
{
    const string sql = """
        SELECT p.*, c.*
        FROM Products p
        INNER JOIN Categories c ON p.CategoryId = c.Id
        WHERE p.Id = @Id
        """;

    using var connection = _factory.CreateConnection();

    var result = await connection.QueryAsync<Product, Category, Product>(
        sql,
        (product, category) =>
        {
            product.Category = category;
            return product;
        },
        new { Id = id },
        splitOn: "Id");  // 发生拆分的列

    return result.FirstOrDefault();
}

// 一对多映射
public async Task<Order?> GetOrderWithItemsAsync(int orderId)
{
    const string sql = """
        SELECT o.*, oi.*, p.*
        FROM Orders o
        LEFT JOIN OrderItems oi ON o.Id = oi.OrderId
        LEFT JOIN Products p ON oi.ProductId = p.Id
        WHERE o.Id = @OrderId
        """;

    var orderDictionary = new Dictionary<int, Order>();

    using var connection = _factory.CreateConnection();

    await connection.QueryAsync<Order, OrderItem, Product, Order>(
        sql,
        (order, item, product) =>
        {
            if (!orderDictionary.TryGetValue(order.Id, out var existingOrder))
            {
                existingOrder = order;
                existingOrder.Items = new List<OrderItem>();
                orderDictionary.Add(order.Id, existingOrder);
            }

            if (item != null)
            {
                item.Product = product;
                existingOrder.Items.Add(item);
            }

            return existingOrder;
        },
        new { OrderId = orderId },
        splitOn: "Id,Id");

    return orderDictionary.Values.FirstOrDefault();
}
```

### 6. 多个结果集

```csharp
public async Task<(IReadOnlyList<Product> Products, int TotalCount)> SearchWithCountAsync(
    ProductSearchCriteria criteria)
{
    const string sql = """
        -- 第一个结果集：计数
        SELECT COUNT(*) FROM Products WHERE CategoryId = @CategoryId;

        -- 第二个结果集：数据
        SELECT * FROM Products
        WHERE CategoryId = @CategoryId
        ORDER BY Name
        OFFSET @Offset ROWS FETCH NEXT @PageSize ROWS ONLY;
        """;

    using var connection = _factory.CreateConnection();
    using var multi = await connection.QueryMultipleAsync(sql, new
    {
        CategoryId = criteria.CategoryId,
        Offset = (criteria.Page - 1) * criteria.PageSize,
        PageSize = criteria.PageSize
    });

    var totalCount = await multi.ReadSingleAsync<int>();
    var products = (await multi.ReadAsync<Product>()).ToList();

    return (products, totalCount);
}
```

## 高级模式

### 7. 表值参数（批量操作）

```csharp
// SQL Server TVP 用于批量操作
public async Task<IReadOnlyList<Product>> GetByIdsAsync(IEnumerable<string> ids)
{
    // 创建匹配 TVP 结构的 DataTable
    var table = new DataTable();
    table.Columns.Add("Id", typeof(string));

    foreach (var id in ids)
    {
        table.Rows.Add(id);
    }

    using var connection = _factory.CreateConnection();

    var results = await connection.QueryAsync<Product>(
        "SELECT p.* FROM Products p INNER JOIN @Ids i ON p.Id = i.Id",
        new { Ids = table.AsTableValuedParameter("dbo.StringIdList") });

    return results.ToList();
}

// 用于创建 TVP 类型的 SQL：
// CREATE TYPE dbo.StringIdList AS TABLE (Id NVARCHAR(40));
```

### 8. 存储过程

```csharp
public async Task<IReadOnlyList<Product>> GetTopProductsAsync(int categoryId, int count)
{
    using var connection = _factory.CreateConnection();

    var results = await connection.QueryAsync<Product>(
        "dbo.GetTopProductsByCategory",
        new { CategoryId = categoryId, TopN = count },
        commandType: CommandType.StoredProcedure);

    return results.ToList();
}

// 带输出参数
public async Task<(Order Order, string ConfirmationCode)> CreateOrderAsync(Order order)
{
    var parameters = new DynamicParameters(new
    {
        order.CustomerId,
        order.Total
    });
    parameters.Add("OrderId", dbType: DbType.Int32, direction: ParameterDirection.Output);
    parameters.Add("ConfirmationCode", dbType: DbType.String, size: 20, direction: ParameterDirection.Output);

    using var connection = _factory.CreateConnection();

    await connection.ExecuteAsync(
        "dbo.CreateOrder",
        parameters,
        commandType: CommandType.StoredProcedure);

    order.Id = parameters.Get<int>("OrderId");
    var confirmationCode = parameters.Get<string>("ConfirmationCode");

    return (order, confirmationCode);
}
```

### 9. 事务

```csharp
public async Task<Order> CreateOrderWithItemsAsync(Order order, List<OrderItem> items)
{
    using var connection = _factory.CreateConnection();
    await connection.OpenAsync();

    using var transaction = await connection.BeginTransactionAsync();

    try
    {
        // 插入订单
        order.Id = await connection.QuerySingleAsync<int>(
            """
            INSERT INTO Orders (CustomerId, Total, CreatedAt)
            OUTPUT INSERTED.Id
            VALUES (@CustomerId, @Total, @CreatedAt)
            """,
            order,
            transaction);

        // 插入订单项
        foreach (var item in items)
        {
            item.OrderId = order.Id;
        }

        await connection.ExecuteAsync(
            """
            INSERT INTO OrderItems (OrderId, ProductId, Quantity, UnitPrice)
            VALUES (@OrderId, @ProductId, @Quantity, @UnitPrice)
            """,
            items,
            transaction);

        await transaction.CommitAsync();

        order.Items = items;
        return order;
    }
    catch
    {
        await transaction.RollbackAsync();
        throw;
    }
}
```

### 10. 自定义类型处理器

```csharp
// 为 JSON 列注册自定义类型处理器
public class JsonTypeHandler<T> : SqlMapper.TypeHandler<T>
{
    public override T Parse(object value)
    {
        if (value is string json)
        {
            return JsonSerializer.Deserialize<T>(json)!;
        }
        return default!;
    }

    public override void SetValue(IDbDataParameter parameter, T value)
    {
        parameter.Value = JsonSerializer.Serialize(value);
        parameter.DbType = DbType.String;
    }
}

// 在启动时注册
SqlMapper.AddTypeHandler(new JsonTypeHandler<ProductMetadata>());

// 现在可以直接查询
var product = await connection.QueryFirstAsync<Product>(
    "SELECT Id, Name, Metadata FROM Products WHERE Id = @Id",
    new { Id = id });
// product.Metadata 从 JSON 自动反序列化
```

## 性能提示

### 11. 使用 CommandDefinition 进行取消

```csharp
// 始终对异步操作使用 CommandDefinition
var result = await connection.QueryAsync<Product>(
    new CommandDefinition(
        commandText: "SELECT * FROM Products WHERE CategoryId = @CategoryId",
        parameters: new { CategoryId = categoryId },
        cancellationToken: ct,
        commandTimeout: 30));
```

### 12. 缓冲 vs 非缓冲查询

```csharp
// 缓冲（默认）- 将所有结果加载到内存中
var products = await connection.QueryAsync<Product>(sql);  // 返回列表

// 非缓冲 - 流式传输结果（大型结果集的内存占用更低）
var products = await connection.QueryUnbufferedAsync<Product>(sql);  // 返回 IAsyncEnumerable

await foreach (var product in products)
{
    // 每次处理一个
}
```

### 13. 连接池设置

```json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=MyDb;User Id=sa;Password=xxx;TrustServerCertificate=True;Min Pool Size=5;Max Pool Size=100;Connection Timeout=30;"
  }
}
```

## 常见模式

### 仓储基类

```csharp
public abstract class DapperRepositoryBase<T> where T : class
{
    protected readonly IDbConnectionFactory ConnectionFactory;
    protected readonly ILogger Logger;
    protected abstract string TableName { get; }

    protected DapperRepositoryBase(IDbConnectionFactory factory, ILogger logger)
    {
        ConnectionFactory = factory;
        Logger = logger;
    }

    protected async Task<T?> GetByIdAsync<TId>(TId id, CancellationToken ct = default)
    {
        var sql = $"SELECT * FROM {TableName} WHERE Id = @Id";

        using var connection = ConnectionFactory.CreateConnection();
        return await connection.QueryFirstOrDefaultAsync<T>(
            new CommandDefinition(sql, new { Id = id }, cancellationToken: ct));
    }

    protected async Task<IReadOnlyList<T>> GetAllAsync(CancellationToken ct = default)
    {
        var sql = $"SELECT * FROM {TableName}";

        using var connection = ConnectionFactory.CreateConnection();
        var results = await connection.QueryAsync<T>(
            new CommandDefinition(sql, cancellationToken: ct));

        return results.ToList();
    }

    protected async Task<int> ExecuteAsync(
        string sql,
        object? parameters = null,
        CancellationToken ct = default)
    {
        using var connection = ConnectionFactory.CreateConnection();
        return await connection.ExecuteAsync(
            new CommandDefinition(sql, parameters, cancellationToken: ct));
    }
}
```

## 避免的反模式

```csharp
// ❌ 不好 - SQL 注入风险
var sql = $"SELECT * FROM Products WHERE Name = '{userInput}'";

// ✅ 好 - 参数化查询
var sql = "SELECT * FROM Products WHERE Name = @Name";
await connection.QueryAsync<Product>(sql, new { Name = userInput });

// ❌ 不好 - 未释放连接
var connection = new SqlConnection(connectionString);
var result = await connection.QueryAsync<Product>(sql);
// 连接泄漏！

// ✅ 好 - Using 语句
using var connection = new SqlConnection(connectionString);
var result = await connection.QueryAsync<Product>(sql);

// ❌ 不好 - 不需要时手动打开连接
await connection.OpenAsync();  // Dapper 自动执行此操作
var result = await connection.QueryAsync<Product>(sql);

// ✅ 好 - 让 Dapper 管理连接
var result = await connection.QueryAsync<Product>(sql);
```
