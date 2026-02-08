# Entity Framework Core 最佳实践

生产应用程序中 EF Core 的性能优化和最佳实践。

## 查询优化

### 1. 对只读查询使用 AsNoTracking

```csharp
// ✅ 好 - 无更改跟踪开销
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(ct);

// ❌ 不好 - 只读数据的不必要跟踪
var products = await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(ct);
```

### 2. 仅选择所需列

```csharp
// ✅ 好 - 投影到 DTO
var products = await _context.Products
    .AsNoTracking()
    .Where(p => p.CategoryId == categoryId)
    .Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        Price = p.Price
    })
    .ToListAsync(ct);

// ❌ 不好 - 获取所有列
var products = await _context.Products
    .Where(p => p.CategoryId == categoryId)
    .ToListAsync(ct);
```

### 3. 使用预加载避免 N+1 查询

```csharp
// ✅ 好 - 使用 Include 的单个查询
var orders = await _context.Orders
    .AsNoTracking()
    .Include(o => o.Items)
        .ThenInclude(i => i.Product)
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(ct);

// ❌ 不好 - N+1 查询（延迟加载）
var orders = await _context.Orders
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(ct);

foreach (var order in orders)
{
    // 每次迭代触发单独的查询！
    var items = order.Items.ToList();
}
```

### 4. 对大型 Include 使用拆分查询

```csharp
// ✅ 好 - 防止笛卡尔爆炸
var orders = await _context.Orders
    .AsNoTracking()
    .Include(o => o.Items)
    .Include(o => o.Payments)
    .Include(o => o.ShippingHistory)
    .AsSplitQuery()  // 作为多个查询执行
    .Where(o => o.CustomerId == customerId)
    .ToListAsync(ct);
```

### 5. 为热路径使用编译查询

```csharp
public class ProductRepository
{
    // 编译一次，多次重用
    private static readonly Func<AppDbContext, string, Task<Product?>> GetByIdQuery =
        EF.CompileAsyncQuery((AppDbContext ctx, string id) =>
            ctx.Products.AsNoTracking().FirstOrDefault(p => p.Id == id));

    private static readonly Func<AppDbContext, int, IAsyncEnumerable<Product>> GetByCategoryQuery =
        EF.CompileAsyncQuery((AppDbContext ctx, int categoryId) =>
            ctx.Products.AsNoTracking().Where(p => p.CategoryId == categoryId));

    public Task<Product?> GetByIdAsync(string id, CancellationToken ct)
        => GetByIdQuery(_context, id);

    public IAsyncEnumerable<Product> GetByCategoryAsync(int categoryId)
        => GetByCategoryQuery(_context, categoryId);
}
```

## 批量操作

### 6. 使用 ExecuteUpdate/ExecuteDelete（.NET 7+）

```csharp
// ✅ 好 - 单个 SQL UPDATE
await _context.Products
    .Where(p => p.CategoryId == oldCategoryId)
    .ExecuteUpdateAsync(s => s
        .SetProperty(p => p.CategoryId, newCategoryId)
        .SetProperty(p => p.UpdatedAt, DateTime.UtcNow),
        ct);

// ✅ 好 - 单个 SQL DELETE
await _context.Products
    .Where(p => p.IsDeleted && p.UpdatedAt < cutoffDate)
    .ExecuteDeleteAsync(ct);

// ❌ 不好 - 将所有实体加载到内存中
var products = await _context.Products
    .Where(p => p.CategoryId == oldCategoryId)
    .ToListAsync(ct);

foreach (var product in products)
{
    product.CategoryId = newCategoryId;
}
await _context.SaveChangesAsync(ct);
```

### 7. 使用 EFCore.BulkExtensions 批量插入

```csharp
// 使用 EFCore.BulkExtensions 包
var products = GenerateLargeProductList();

// ✅ 好 - 批量插入（对于大型数据集快得多）
await _context.BulkInsertAsync(products, ct);

// ❌ 不好 - 单个插入
foreach (var product in products)
{
    _context.Products.Add(product);
}
await _context.SaveChangesAsync(ct);
```

## 连接管理

### 8. 配置连接池

```csharp
services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString, sqlOptions =>
    {
        sqlOptions.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(10),
            errorNumbersToAdd: null);

        sqlOptions.CommandTimeout(30);
    });

    // 性能设置
    options.UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking);

    // 仅开发环境
    if (env.IsDevelopment())
    {
        options.EnableSensitiveDataLogging();
        options.EnableDetailedErrors();
    }
});
```

### 9. 使用 DbContext 池

```csharp
// ✅ 好 - Context 池（减少分配开销）
services.AddDbContextPool<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString);
}, poolSize: 128);

// 代替 AddDbContext
```

## 并发和事务

### 10. 使用行版本控制处理并发

```csharp
public class Product
{
    public string Id { get; set; }
    public string Name { get; set; }

    [Timestamp]
    public byte[] RowVersion { get; set; }  // SQL Server rowversion
}

// 或使用 Fluent API
builder.Property(p => p.RowVersion)
    .IsRowVersion();

// 处理并发冲突
try
{
    await _context.SaveChangesAsync(ct);
}
catch (DbUpdateConcurrencyException ex)
{
    var entry = ex.Entries.Single();
    var databaseValues = await entry.GetDatabaseValuesAsync(ct);

    if (databaseValues == null)
    {
        // 实体已被删除
        throw new NotFoundException("产品已被另一个用户删除");
    }

    // 客户端优先 - 覆盖数据库值
    entry.OriginalValues.SetValues(databaseValues);
    await _context.SaveChangesAsync(ct);
}
```

### 11. 需要时使用显式事务

```csharp
await using var transaction = await _context.Database.BeginTransactionAsync(ct);

try
{
    // 多个操作
    _context.Orders.Add(order);
    await _context.SaveChangesAsync(ct);

    await _context.OrderItems.AddRangeAsync(items, ct);
    await _context.SaveChangesAsync(ct);

    await _paymentService.ProcessAsync(order.Id, ct);

    await transaction.CommitAsync(ct);
}
catch
{
    await transaction.RollbackAsync(ct);
    throw;
}
```

## 索引策略

### 12. 为查询模式创建索引

```csharp
public class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        // 唯一索引
        builder.HasIndex(p => p.Sku)
            .IsUnique();

        // 常见查询模式的复合索引
        builder.HasIndex(p => new { p.CategoryId, p.Name });

        // 筛选索引（SQL Server）
        builder.HasIndex(p => p.Price)
            .HasFilter("[IsDeleted] = 0");

        // 包含列的覆盖索引
        builder.HasIndex(p => p.CategoryId)
            .IncludeProperties(p => new { p.Name, p.Price });
    }
}
```

## 避免的常见反模式

### ❌ 过早调用 ToList()

```csharp
// ❌ 不好 - 在内存中过滤之前获取所有产品
var products = _context.Products.ToList()
    .Where(p => p.Price > 100);

// ✅ 好 - 在 SQL 中过滤
var products = await _context.Products
    .Where(p => p.Price > 100)
    .ToListAsync(ct);
```

### ❌ 对大型集合使用 Contains

```csharp
// ❌ 不好 - 生成巨大的 IN 子句
var ids = GetThousandsOfIds();
var products = await _context.Products
    .Where(p => ids.Contains(p.Id))
    .ToListAsync(ct);

// ✅ 好 - 使用临时表或批量查询
var products = new List<Product>();
foreach (var batch in ids.Chunk(100))
{
    var batchResults = await _context.Products
        .Where(p => batch.Contains(p.Id))
        .ToListAsync(ct);
    products.AddRange(batchResults);
}
```

### ❌ 查询中的字符串连接

```csharp
// ❌ 不好 - 无法使用索引
var products = await _context.Products
    .Where(p => (p.FirstName + " " + p.LastName).Contains(searchTerm))
    .ToListAsync(ct);

// ✅ 好 - 使用带索引的计算列
builder.Property(p => p.FullName)
    .HasComputedColumnSql("[FirstName] + ' ' + [LastName]");
builder.HasIndex(p => p.FullName);
```

## 监控和诊断

```csharp
// 记录慢查询
services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(connectionString);

    options.LogTo(
        filter: (eventId, level) => eventId.Id == CoreEventId.QueryExecutionPlanned.Id,
        logger: (eventData) =>
        {
            if (eventData is QueryExpressionEventData queryData)
            {
                var duration = queryData.Duration;
                if (duration > TimeSpan.FromSeconds(1))
                {
                    _logger.LogWarning("检测到慢查询：{Duration}ms - {Query}",
                        duration.TotalMilliseconds,
                        queryData.Expression);
                }
            }
        });
});
```
