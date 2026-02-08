# 调试和追踪配置

你是一位专注于设置综合调试环境、分布式追踪和诊断工具的调试专家。配置调试工作流、实现追踪解决方案，并建立开发和生产环境的故障排除实践。

## 上下文

用户需要设置调试和追踪功能以高效诊断问题、定位错误并理解系统行为。专注于开发者生产力、生产调试、分布式追踪和综合日志策略。

## 需求

$ARGUMENTS

## 指令

### 1. 开发环境调试

设置综合调试环境：

**VS Code 调试配置**

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Node.js App",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "node",
      "runtimeArgs": ["--inspect-brk", "--enable-source-maps"],
      "program": "${workspaceFolder}/src/index.js",
      "env": {
        "NODE_ENV": "development",
        "DEBUG": "*",
        "NODE_OPTIONS": "--max-old-space-size=4096"
      },
      "sourceMaps": true,
      "resolveSourceMapLocations": [
        "${workspaceFolder}/**",
        "!**/node_modules/**"
      ],
      "skipFiles": ["<node_internals>/**", "node_modules/**"],
      "console": "integratedTerminal",
      "outputCapture": "std"
    },
    {
      "name": "Debug TypeScript",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "sourceMaps": true,
      "smartStep": true,
      "internalConsoleOptions": "openOnSessionStart"
    },
    {
      "name": "Debug Jest Tests",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/jest",
      "args": [
        "--runInBand",
        "--no-cache",
        "--watchAll=false",
        "--detectOpenHandles"
      ],
      "console": "integratedTerminal",
      "internalConsoleOptions": "neverOpen",
      "env": {
        "NODE_ENV": "test"
      }
    },
    {
      "name": "Attach to Process",
      "type": "node",
      "request": "attach",
      "processId": "${command:PickProcess}",
      "protocol": "inspector",
      "restart": true,
      "sourceMaps": true
    }
  ],
  "compounds": [
    {
      "name": "Full Stack Debug",
      "configurations": ["Debug Backend", "Debug Frontend"],
      "stopAll": true
    }
  ]
}
```

**Chrome DevTools 配置**

```javascript
// debug-helpers.js
class DebugHelper {
  constructor() {
    this.setupDevTools();
    this.setupConsoleHelpers();
    this.setupPerformanceMarkers();
  }

  setupDevTools() {
    if (typeof window !== "undefined") {
      // 添加调试命名空间
      window.DEBUG = window.DEBUG || {};

      // 存储重要对象的引用
      window.DEBUG.store = () => window.__REDUX_STORE__;
      window.DEBUG.router = () => window.__ROUTER__;
      window.DEBUG.components = new Map();

      // 性能调试
      window.DEBUG.measureRender = (componentName) => {
        performance.mark(`${componentName}-start`);
        return () => {
          performance.mark(`${componentName}-end`);
          performance.measure(
            componentName,
            `${componentName}-start`,
            `${componentName}-end`,
          );
        };
      };

      // 内存调试
      window.DEBUG.heapSnapshot = async () => {
        if ("memory" in performance) {
          const snapshot = await performance.measureUserAgentSpecificMemory();
          console.table(snapshot);
          return snapshot;
        }
      };
    }
  }

  setupConsoleHelpers() {
    // 增强的控制台日志
    const styles = {
      error: "color: #ff0000; font-weight: bold;",
      warn: "color: #ff9800; font-weight: bold;",
      info: "color: #2196f3; font-weight: bold;",
      debug: "color: #4caf50; font-weight: bold;",
      trace: "color: #9c27b0; font-weight: bold;",
    };

    Object.entries(styles).forEach(([level, style]) => {
      const original = console[level];
      console[level] = function (...args) {
        if (process.env.NODE_ENV === "development") {
          const timestamp = new Date().toISOString();
          original.call(
            console,
            `%c[${timestamp}] ${level.toUpperCase()}:`,
            style,
            ...args,
          );
        }
      };
    });
  }
}

// React DevTools 集成
if (process.env.NODE_ENV === "development") {
  // 暴露 React 内部
  window.__REACT_DEVTOOLS_GLOBAL_HOOK__ = {
    ...window.__REACT_DEVTOOLS_GLOBAL_HOOK__,
    onCommitFiberRoot: (id, root) => {
      // 自定义提交日志
      console.debug("React commit:", root);
    },
  };
}
```

### 2. 远程调试设置

配置远程调试功能：

**远程调试服务器**

```javascript
// remote-debug-server.js
const inspector = require('inspector');
const WebSocket = require('ws');
const http = require('http');

class RemoteDebugServer {
    constructor(options = {}) {
        this.port = options.port || 9229;
        this.host = options.host || '0.0.0.0';
        this.wsPort = options.wsPort || 9230;
        this.sessions = new Map();
    }

    start() {
        // 打开检查器
        inspector.open(this.port, this.host, true);

        // 为远程连接创建 WebSocket 服务器
        this.wss = new WebSocket.Server({ port: this.wsPort });

        this.wss.on('connection', (ws) => {
            const sessionId = this.generateSessionId();
            this.sessions.set(sessionId, ws);

            ws.on('message', (message) => {
                this.handleDebugCommand(sessionId, message);
            });

            ws.on('close', () => {
                this.sessions.delete(sessionId);
            });

            // 发送初始会话信息
            ws.send(JSON.stringify({
                type: 'session',
                sessionId,
                debugUrl: `chrome-devtools://devtools/bundled/inspector.html?ws=${this.host}:${this.port}`
            }));
        });

        console.log(`Remote debug server listening on ws://${this.host}:${this.wsPort}`);
    }

    handleDebugCommand(sessionId, message) {
        const command = JSON.parse(message);

        switch (command.type) {
            case 'evaluate':
                this.evaluateExpression(sessionId, command.expression);
                break;
            case 'setBreakpoint':
                this.setBreakpoint(command.file, command.line);
                break;
            case 'heapSnapshot':
                this.takeHeapSnapshot(sessionId);
                break;
            case 'profile':
                this.startProfiling(sessionId, command.duration);
                break;
        }
    }

    evaluateExpression(sessionId, expression) {
        const session = new inspector.Session();
        session.connect();

        session.post('Runtime.evaluate', {
            expression,
            generatePreview: true,
            includeCommandLineAPI: true
        }, (error, result) => {
            const ws = this.sessions.get(sessionId);
            if (ws) {
                ws.send(JSON.stringify({
                    type: 'evaluateResult',
                    result: result || error
                }));
            }
        });

        session.disconnect();
    }
}

// Docker 远程调试设置
FROM node:18
RUN apt-get update && apt-get install -y \
    chromium \
    gdb \
    strace \
    tcpdump \
    vim

EXPOSE 9229 9230
ENV NODE_OPTIONS="--inspect=0.0.0.0:9229"
CMD ["node", "--inspect-brk=0.0.0.0:9229", "index.js"]
```

### 3. 分布式追踪

实现综合的分布式追踪：

**OpenTelemetry 设置**

```javascript
// tracing.js
const { NodeSDK } = require("@opentelemetry/sdk-node");
const {
  getNodeAutoInstrumentations,
} = require("@opentelemetry/auto-instrumentations-node");
const { Resource } = require("@opentelemetry/resources");
const {
  SemanticResourceAttributes,
} = require("@opentelemetry/semantic-conventions");
const { JaegerExporter } = require("@opentelemetry/exporter-jaeger");
const { BatchSpanProcessor } = require("@opentelemetry/sdk-trace-base");

class TracingSystem {
  constructor(serviceName) {
    this.serviceName = serviceName;
    this.sdk = null;
  }

  initialize() {
    const jaegerExporter = new JaegerExporter({
      endpoint:
        process.env.JAEGER_ENDPOINT || "http://localhost:14268/api/traces",
    });

    const resource = Resource.default().merge(
      new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: this.serviceName,
        [SemanticResourceAttributes.SERVICE_VERSION]:
          process.env.SERVICE_VERSION || "1.0.0",
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]:
          process.env.NODE_ENV || "development",
      }),
    );

    this.sdk = new NodeSDK({
      resource,
      spanProcessor: new BatchSpanProcessor(jaegerExporter),
      instrumentations: [
        getNodeAutoInstrumentations({
          "@opentelemetry/instrumentation-fs": {
            enabled: false, // 太嘈杂
          },
          "@opentelemetry/instrumentation-http": {
            requestHook: (span, request) => {
              span.setAttribute(
                "http.request.body",
                JSON.stringify(request.body),
              );
            },
            responseHook: (span, response) => {
              span.setAttribute("http.response.size", response.length);
            },
          },
          "@opentelemetry/instrumentation-express": {
            requestHook: (span, req) => {
              span.setAttribute("user.id", req.user?.id);
              span.setAttribute("session.id", req.session?.id);
            },
          },
        }),
      ],
    });

    this.sdk.start();

    // 优雅关闭
    process.on("SIGTERM", () => {
      this.sdk
        .shutdown()
        .then(() => console.log("Tracing terminated"))
        .catch((error) => console.error("Error terminating tracing", error))
        .finally(() => process.exit(0));
    });
  }

  // 自定义 span 创建
  createSpan(name, fn, attributes = {}) {
    const tracer = trace.getTracer(this.serviceName);
    return tracer.startActiveSpan(name, async (span) => {
      try {
        // 添加自定义属性
        Object.entries(attributes).forEach(([key, value]) => {
          span.setAttribute(key, value);
        });

        // 执行函数
        const result = await fn(span);

        span.setStatus({ code: SpanStatusCode.OK });
        return result;
      } catch (error) {
        span.recordException(error);
        span.setStatus({
          code: SpanStatusCode.ERROR,
          message: error.message,
        });
        throw error;
      } finally {
        span.end();
      }
    });
  }
}

// 分布式追踪中间件
class TracingMiddleware {
  constructor() {
    this.tracer = trace.getTracer("http-middleware");
  }

  express() {
    return (req, res, next) => {
      const span = this.tracer.startSpan(`${req.method} ${req.path}`, {
        kind: SpanKind.SERVER,
        attributes: {
          "http.method": req.method,
          "http.url": req.url,
          "http.target": req.path,
          "http.host": req.hostname,
          "http.scheme": req.protocol,
          "http.user_agent": req.get("user-agent"),
          "http.request_content_length": req.get("content-length"),
        },
      });

      // 将追踪上下文注入请求
      req.span = span;
      req.traceId = span.spanContext().traceId;

      // 将追踪 ID 添加到响应头
      res.setHeader("X-Trace-Id", req.traceId);

      // 覆盖 res.end 以捕获响应数据
      const originalEnd = res.end;
      res.end = function (...args) {
        span.setAttribute("http.status_code", res.statusCode);
        span.setAttribute(
          "http.response_content_length",
          res.get("content-length"),
        );

        if (res.statusCode >= 400) {
          span.setStatus({
            code: SpanStatusCode.ERROR,
            message: `HTTP ${res.statusCode}`,
          });
        }

        span.end();
        originalEnd.apply(res, args);
      };

      next();
    };
  }
}
```

### 4. 调试日志框架

实现结构化调试日志：

**高级日志记录器**

```javascript
// debug-logger.js
const winston = require("winston");
const { ElasticsearchTransport } = require("winston-elasticsearch");

class DebugLogger {
  constructor(options = {}) {
    this.service = options.service || "app";
    this.level = process.env.LOG_LEVEL || "debug";
    this.logger = this.createLogger();
  }

  createLogger() {
    const formats = [
      winston.format.timestamp(),
      winston.format.errors({ stack: true }),
      winston.format.splat(),
      winston.format.json(),
    ];

    if (process.env.NODE_ENV === "development") {
      formats.push(winston.format.colorize());
      formats.push(winston.format.printf(this.devFormat));
    }

    const transports = [
      new winston.transports.Console({
        level: this.level,
        handleExceptions: true,
        handleRejections: true,
      }),
    ];

    // 为调试添加文件传输
    if (process.env.DEBUG_LOG_FILE) {
      transports.push(
        new winston.transports.File({
          filename: process.env.DEBUG_LOG_FILE,
          level: "debug",
          maxsize: 10485760, // 10MB
          maxFiles: 5,
        }),
      );
    }

    // 为生产添加 Elasticsearch
    if (process.env.ELASTICSEARCH_URL) {
      transports.push(
        new ElasticsearchTransport({
          level: "info",
          clientOpts: {
            node: process.env.ELASTICSEARCH_URL,
          },
          index: `logs-${this.service}`,
        }),
      );
    }

    return winston.createLogger({
      level: this.level,
      format: winston.format.combine(...formats),
      defaultMeta: {
        service: this.service,
        environment: process.env.NODE_ENV,
        hostname: require("os").hostname(),
        pid: process.pid,
      },
      transports,
    });
  }

  devFormat(info) {
    const { timestamp, level, message, ...meta } = info;
    const metaString = Object.keys(meta).length
      ? "\n" + JSON.stringify(meta, null, 2)
      : "";

    return `${timestamp} [${level}]: ${message}${metaString}`;
  }

  // 调试专用方法
  trace(message, meta = {}) {
    const stack = new Error().stack;
    this.logger.debug(message, {
      ...meta,
      trace: stack,
      timestamp: Date.now(),
    });
  }

  timing(label, fn) {
    const start = process.hrtime.bigint();
    const result = fn();
    const end = process.hrtime.bigint();
    const duration = Number(end - start) / 1000000; // 转换为毫秒

    this.logger.debug(`Timing: ${label}`, {
      duration,
      unit: "ms",
    });

    return result;
  }

  memory() {
    const usage = process.memoryUsage();
    this.logger.debug("Memory usage", {
      rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
      heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)}MB`,
      heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
      external: `${Math.round(usage.external / 1024 / 1024)}MB`,
    });
  }
}

// 调试上下文管理器
class DebugContext {
  constructor() {
    this.contexts = new Map();
  }

  create(id, metadata = {}) {
    const context = {
      id,
      startTime: Date.now(),
      metadata,
      logs: [],
      spans: [],
    };

    this.contexts.set(id, context);
    return context;
  }

  log(contextId, level, message, data = {}) {
    const context = this.contexts.get(contextId);
    if (context) {
      context.logs.push({
        timestamp: Date.now(),
        level,
        message,
        data,
      });
    }
  }

  export(contextId) {
    const context = this.contexts.get(contextId);
    if (!context) return null;

    return {
      ...context,
      duration: Date.now() - context.startTime,
      logCount: context.logs.length,
    };
  }
}
```

### 5. Source Map 配置

设置生产调试的 source map 支持：

**Source Map 设置**

```javascript
// webpack.config.js
module.exports = {
  mode: "production",
  devtool: "hidden-source-map", // 生成 source maps 但不引用它们

  output: {
    filename: "[name].[contenthash].js",
    sourceMapFilename: "sourcemaps/[name].[contenthash].js.map",
  },

  plugins: [
    // 上传 source maps 到错误跟踪服务
    new SentryWebpackPlugin({
      authToken: process.env.SENTRY_AUTH_TOKEN,
      org: "your-org",
      project: "your-project",
      include: "./dist",
      ignore: ["node_modules"],
      urlPrefix: "~/",
      release: process.env.RELEASE_VERSION,
      deleteAfterCompile: true,
    }),
  ],
};

// 运行时 source map 支持
require("source-map-support").install({
  environment: "node",
  handleUncaughtExceptions: false,
  retrieveSourceMap(source) {
    // 生产环境的自定义 source map 检索
    if (process.env.NODE_ENV === "production") {
      const sourceMapUrl = getSourceMapUrl(source);
      if (sourceMapUrl) {
        const map = fetchSourceMap(sourceMapUrl);
        return {
          url: source,
          map: map,
        };
      }
    }
    return null;
  },
});

// 堆栈跟踪增强
Error.prepareStackTrace = (error, stack) => {
  const mapped = stack.map((frame) => {
    const fileName = frame.getFileName();
    const lineNumber = frame.getLineNumber();
    const columnNumber = frame.getColumnNumber();

    // 尝试获取原始位置
    const original = getOriginalPosition(fileName, lineNumber, columnNumber);

    return {
      function: frame.getFunctionName() || "<anonymous>",
      file: original?.source || fileName,
      line: original?.line || lineNumber,
      column: original?.column || columnNumber,
      native: frame.isNative(),
      async: frame.isAsync(),
    };
  });

  return {
    message: error.message,
    stack: mapped,
  };
};
```

### 6. 性能分析

实现性能分析工具：

**性能分析器**

```javascript
// performance-profiler.js
const v8Profiler = require("v8-profiler-next");
const fs = require("fs");
const path = require("path");

class PerformanceProfiler {
  constructor(options = {}) {
    this.outputDir = options.outputDir || "./profiles";
    this.profiles = new Map();

    // 确保输出目录存在
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
  }

  startCPUProfile(id, options = {}) {
    const title = options.title || `cpu-profile-${id}`;
    v8Profiler.startProfiling(title, true);

    this.profiles.set(id, {
      type: "cpu",
      title,
      startTime: Date.now(),
    });

    return id;
  }

  stopCPUProfile(id) {
    const profileInfo = this.profiles.get(id);
    if (!profileInfo || profileInfo.type !== "cpu") {
      throw new Error(`CPU profile ${id} not found`);
    }

    const profile = v8Profiler.stopProfiling(profileInfo.title);
    const duration = Date.now() - profileInfo.startTime;

    // 导出 profile
    const fileName = `${profileInfo.title}-${Date.now()}.cpuprofile`;
    const filePath = path.join(this.outputDir, fileName);

    profile.export((error, result) => {
      if (!error) {
        fs.writeFileSync(filePath, result);
        console.log(`CPU profile saved to ${filePath}`);
      }
      profile.delete();
    });

    this.profiles.delete(id);

    return {
      id,
      duration,
      filePath,
    };
  }

  takeHeapSnapshot(tag = "") {
    const fileName = `heap-${tag}-${Date.now()}.heapsnapshot`;
    const filePath = path.join(this.outputDir, fileName);

    const snapshot = v8Profiler.takeSnapshot();

    // 导出 snapshot
    snapshot.export((error, result) => {
      if (!error) {
        fs.writeFileSync(filePath, result);
        console.log(`Heap snapshot saved to ${filePath}`);
      }
      snapshot.delete();
    });

    return filePath;
  }

  measureFunction(fn, name = "anonymous") {
    const measurements = {
      name,
      executions: 0,
      totalTime: 0,
      minTime: Infinity,
      maxTime: 0,
      avgTime: 0,
      lastExecution: null,
    };

    return new Proxy(fn, {
      apply(target, thisArg, args) {
        const start = process.hrtime.bigint();

        try {
          const result = target.apply(thisArg, args);

          if (result instanceof Promise) {
            return result.finally(() => {
              this.recordExecution(start);
            });
          }

          this.recordExecution(start);
          return result;
        } catch (error) {
          this.recordExecution(start);
          throw error;
        }
      },

      recordExecution(start) {
        const end = process.hrtime.bigint();
        const duration = Number(end - start) / 1000000; // 转换为毫秒

        measurements.executions++;
        measurements.totalTime += duration;
        measurements.minTime = Math.min(measurements.minTime, duration);
        measurements.maxTime = Math.max(measurements.maxTime, duration);
        measurements.avgTime = measurements.totalTime / measurements.executions;
        measurements.lastExecution = new Date();

        // 记录慢执行
        if (duration > 100) {
          console.warn(`Slow function execution: ${name} took ${duration}ms`);
        }
      },

      get(target, prop) {
        if (prop === "measurements") {
          return measurements;
        }
        return target[prop];
      },
    });
  }
}

// 内存泄漏检测器
class MemoryLeakDetector {
  constructor() {
    this.snapshots = [];
    this.threshold = 50 * 1024 * 1024; // 50MB
  }

  start(interval = 60000) {
    this.interval = setInterval(() => {
      this.checkMemory();
    }, interval);
  }

  checkMemory() {
    const usage = process.memoryUsage();
    const snapshot = {
      timestamp: Date.now(),
      heapUsed: usage.heapUsed,
      external: usage.external,
      rss: usage.rss,
    };

    this.snapshots.push(snapshot);

    // 只保留最近 10 个快照
    if (this.snapshots.length > 10) {
      this.snapshots.shift();
    }

    // 检查内存泄漏模式
    if (this.snapshots.length >= 5) {
      const trend = this.calculateTrend();
      if (trend.increasing && trend.delta > this.threshold) {
        console.error("Potential memory leak detected!", {
          trend,
          current: snapshot,
        });

        // 获取堆快照进行分析
        const profiler = new PerformanceProfiler();
        profiler.takeHeapSnapshot("leak-detection");
      }
    }
  }

  calculateTrend() {
    const recent = this.snapshots.slice(-5);
    const first = recent[0];
    const last = recent[recent.length - 1];

    const delta = last.heapUsed - first.heapUsed;
    const increasing = recent.every(
      (s, i) => i === 0 || s.heapUsed > recent[i - 1].heapUsed,
    );

    return {
      increasing,
      delta,
      rate: (delta / (last.timestamp - first.timestamp)) * 1000 * 60, // 每分钟 MB
    };
  }
}
```

### 7. 调试配置管理

集中化调试配置：

**调试配置**

```javascript
// debug-config.js
class DebugConfiguration {
  constructor() {
    this.config = {
      // 调试级别
      levels: {
        error: 0,
        warn: 1,
        info: 2,
        debug: 3,
        trace: 4,
      },

      // 功能开关
      features: {
        remoteDebugging: process.env.ENABLE_REMOTE_DEBUG === "true",
        tracing: process.env.ENABLE_TRACING === "true",
        profiling: process.env.ENABLE_PROFILING === "true",
        memoryMonitoring: process.env.ENABLE_MEMORY_MONITORING === "true",
      },

      // 调试端点
      endpoints: {
        jaeger: process.env.JAEGER_ENDPOINT || "http://localhost:14268",
        elasticsearch: process.env.ELASTICSEARCH_URL || "http://localhost:9200",
        sentry: process.env.SENTRY_DSN,
      },

      // 采样率
      sampling: {
        traces: parseFloat(process.env.TRACE_SAMPLING_RATE || "0.1"),
        profiles: parseFloat(process.env.PROFILE_SAMPLING_RATE || "0.01"),
        logs: parseFloat(process.env.LOG_SAMPLING_RATE || "1.0"),
      },
    };
  }

  isEnabled(feature) {
    return this.config.features[feature] || false;
  }

  getLevel() {
    const level = process.env.DEBUG_LEVEL || "info";
    return this.config.levels[level] || 2;
  }

  shouldSample(type) {
    const rate = this.config.sampling[type] || 1.0;
    return Math.random() < rate;
  }
}

// 调试中间件工厂
class DebugMiddlewareFactory {
  static create(app, config) {
    const middlewares = [];

    if (config.isEnabled("tracing")) {
      const tracingMiddleware = new TracingMiddleware();
      middlewares.push(tracingMiddleware.express());
    }

    if (config.isEnabled("profiling")) {
      middlewares.push(this.profilingMiddleware());
    }

    if (config.isEnabled("memoryMonitoring")) {
      const detector = new MemoryLeakDetector();
      detector.start();
    }

    // 调试路由
    if (process.env.NODE_ENV === "development") {
      app.get("/debug/heap", (req, res) => {
        const profiler = new PerformanceProfiler();
        const path = profiler.takeHeapSnapshot("manual");
        res.json({ heapSnapshot: path });
      });

      app.get("/debug/profile", async (req, res) => {
        const profiler = new PerformanceProfiler();
        const id = profiler.startCPUProfile("manual");

        setTimeout(() => {
          const result = profiler.stopCPUProfile(id);
          res.json(result);
        }, 10000);
      });

      app.get("/debug/metrics", (req, res) => {
        res.json({
          memory: process.memoryUsage(),
          cpu: process.cpuUsage(),
          uptime: process.uptime(),
        });
      });
    }

    return middlewares;
  }

  static profilingMiddleware() {
    const profiler = new PerformanceProfiler();

    return (req, res, next) => {
      if (Math.random() < 0.01) {
        // 1% 采样
        const id = profiler.startCPUProfile(`request-${Date.now()}`);

        res.on("finish", () => {
          profiler.stopCPUProfile(id);
        });
      }

      next();
    };
  }
}
```

### 8. 生产调试

启用安全的生产调试：

**生产调试工具**

```javascript
// production-debug.js
class ProductionDebugger {
  constructor(options = {}) {
    this.enabled = process.env.PRODUCTION_DEBUG === "true";
    this.authToken = process.env.DEBUG_AUTH_TOKEN;
    this.allowedIPs = (process.env.DEBUG_ALLOWED_IPS || "").split(",");
  }

  middleware() {
    return (req, res, next) => {
      if (!this.enabled) {
        return next();
      }

      // 检查授权
      const token = req.headers["x-debug-token"];
      const ip = req.ip || req.connection.remoteAddress;

      if (token !== this.authToken || !this.allowedIPs.includes(ip)) {
        return next();
      }

      // 添加调试头
      res.setHeader("X-Debug-Enabled", "true");

      // 为此请求启用调试模式
      req.debugMode = true;
      req.debugContext = new DebugContext().create(req.id);

      // 覆盖此请求的 console
      const originalConsole = { ...console };
      ["log", "debug", "info", "warn", "error"].forEach((method) => {
        console[method] = (...args) => {
          req.debugContext.log(req.id, method, args[0], args.slice(1));
          originalConsole[method](...args);
        };
      });

      // 在响应时恢复 console
      res.on("finish", () => {
        Object.assign(console, originalConsole);

        // 如果请求则发送调试信息
        if (req.headers["x-debug-response"] === "true") {
          const debugInfo = req.debugContext.export(req.id);
          res.setHeader("X-Debug-Info", JSON.stringify(debugInfo));
        }
      });

      next();
    };
  }
}

// 生产中的条件断点
class ConditionalBreakpoint {
  constructor(condition, callback) {
    this.condition = condition;
    this.callback = callback;
    this.hits = 0;
  }

  check(context) {
    if (this.condition(context)) {
      this.hits++;

      // 记录断点命中
      console.debug("Conditional breakpoint hit", {
        condition: this.condition.toString(),
        hits: this.hits,
        context,
      });

      // 执行回调
      if (this.callback) {
        this.callback(context);
      }

      // 在生产中，不要真正中断
      if (process.env.NODE_ENV === "production") {
        // 而是获取快照
        const profiler = new PerformanceProfiler();
        profiler.takeHeapSnapshot(`breakpoint-${Date.now()}`);
      } else {
        // 在开发中，使用 debugger
        debugger;
      }
    }
  }
}

// 使用
const breakpoints = new Map();

// 设置条件断点
breakpoints.set(
  "high-memory",
  new ConditionalBreakpoint(
    (context) => context.memoryUsage > 500 * 1024 * 1024, // 500MB
    (context) => {
      console.error("High memory usage detected", context);
      // 发送警报
      alerting.send("high-memory", context);
    },
  ),
);

// 在代码中检查断点
function checkBreakpoints(context) {
  breakpoints.forEach((breakpoint) => {
    breakpoint.check(context);
  });
}
```

### 9. 调试仪表板

创建用于监控的调试仪表板：

**调试仪表板**

```html
<!-- debug-dashboard.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Debug Dashboard</title>
    <style>
      body {
        font-family: monospace;
        background: #1e1e1e;
        color: #d4d4d4;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
      }
      .metric {
        background: #252526;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
      }
      .metric h3 {
        margin: 0 0 10px 0;
        color: #569cd6;
      }
      .chart {
        height: 200px;
        background: #1e1e1e;
        margin: 10px 0;
      }
      .log-entry {
        padding: 5px;
        border-bottom: 1px solid #3e3e3e;
      }
      .error {
        color: #f44747;
      }
      .warn {
        color: #ff9800;
      }
      .info {
        color: #4fc3f7;
      }
      .debug {
        color: #4caf50;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Debug Dashboard</h1>

      <div class="metric">
        <h3>System Metrics</h3>
        <div id="metrics"></div>
      </div>

      <div class="metric">
        <h3>Memory Usage</h3>
        <canvas id="memoryChart" class="chart"></canvas>
      </div>

      <div class="metric">
        <h3>Request Traces</h3>
        <div id="traces"></div>
      </div>

      <div class="metric">
        <h3>Debug Logs</h3>
        <div id="logs"></div>
      </div>
    </div>

    <script>
      // 用于实时更新的 WebSocket 连接
      const ws = new WebSocket("ws://localhost:9231/debug");

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        switch (data.type) {
          case "metrics":
            updateMetrics(data.payload);
            break;
          case "trace":
            addTrace(data.payload);
            break;
          case "log":
            addLog(data.payload);
            break;
        }
      };

      function updateMetrics(metrics) {
        const container = document.getElementById("metrics");
        container.innerHTML = `
                <div>CPU: ${metrics.cpu.percent}%</div>
                <div>Memory: ${metrics.memory.used}MB / ${metrics.memory.total}MB</div>
                <div>Uptime: ${metrics.uptime}s</div>
                <div>Active Requests: ${metrics.activeRequests}</div>
            `;
      }

      function addTrace(trace) {
        const container = document.getElementById("traces");
        const entry = document.createElement("div");
        entry.className = "log-entry";
        entry.innerHTML = `
                <span>${trace.timestamp}</span>
                <span>${trace.method} ${trace.path}</span>
                <span>${trace.duration}ms</span>
                <span>${trace.status}</span>
            `;
        container.insertBefore(entry, container.firstChild);
      }

      function addLog(log) {
        const container = document.getElementById("logs");
        const entry = document.createElement("div");
        entry.className = `log-entry ${log.level}`;
        entry.innerHTML = `
                <span>${log.timestamp}</span>
                <span>[${log.level.toUpperCase()}]</span>
                <span>${log.message}</span>
            `;
        container.insertBefore(entry, container.firstChild);

        // 只保留最近 100 条日志
        while (container.children.length > 100) {
          container.removeChild(container.lastChild);
        }
      }

      // 内存使用图表
      const memoryChart = document
        .getElementById("memoryChart")
        .getContext("2d");
      const memoryData = [];

      function updateMemoryChart(usage) {
        memoryData.push({
          time: new Date(),
          value: usage,
        });

        // 保留最近 50 个点
        if (memoryData.length > 50) {
          memoryData.shift();
        }

        // 绘制图表
        // ... 图表绘制逻辑
      }
    </script>
  </body>
</html>
```

### 10. IDE 集成

配置 IDE 调试功能：

**IDE 调试扩展**

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-vscode.vscode-js-debug",
        "msjsdiag.debugger-for-chrome",
        "ms-vscode.vscode-typescript-tslint-plugin",
        "dbaeumer.vscode-eslint",
        "ms-azuretools.vscode-docker",
        "humao.rest-client",
        "eamodio.gitlens",
        "usernamehw.errorlens",
        "wayou.vscode-todo-highlight",
        "formulahendry.code-runner"
    ]
}

// .vscode/tasks.json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Start Debug Server",
            "type": "npm",
            "script": "debug",
            "problemMatcher": [],
            "presentation": {
                "reveal": "always",
                "panel": "dedicated"
            }
        },
        {
            "label": "Profile Application",
            "type": "shell",
            "command": "node --inspect-brk --cpu-prof --cpu-prof-dir=./profiles ${workspaceFolder}/src/index.js",
            "problemMatcher": []
        },
        {
            "label": "Memory Snapshot",
            "type": "shell",
            "command": "node --inspect --expose-gc ${workspaceFolder}/scripts/heap-snapshot.js",
            "problemMatcher": []
        }
    ]
}
```

## 输出格式

1. **调试配置**：所有调试工具的完整设置
2. **集成指南**：分步集成说明
3. **故障排除手册**：常见调试场景和解决方案
4. **性能基准**：用于比较的指标
5. **调试脚本**：自动化调试实用程序
6. **仪表板设置**：实时调试界面
7. **文档**：团队调试指南
8. **紧急程序**：生产调试协议

专注于创建一个全面的调试环境，以增强开发者生产力并能够在所有环境中快速解决问题。
