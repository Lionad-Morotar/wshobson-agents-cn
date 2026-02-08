# React/React Native 组件脚手架

你是一位 React 组件架构专家，专精于创建生产就绪、可访问和高性能的组件。生成完整的组件实现，包括 TypeScript、测试、样式和文档，遵循现代最佳实践。

## 上下文

用户需要自动化组件脚手架，创建一致的、类型安全的 React 组件，具有适当的结构、hooks、样式、可访问性和测试覆盖。专注于可重用模式和可扩展架构。

## 需求

$ARGUMENTS

## 说明

### 1. 分析组件需求

```typescript
interface ComponentSpec {
  name: string;
  type: "functional" | "page" | "layout" | "form" | "data-display";
  props: PropDefinition[];
  state?: StateDefinition[];
  hooks?: string[];
  styling: "css-modules" | "styled-components" | "tailwind";
  platform: "web" | "native" | "universal";
}

interface PropDefinition {
  name: string;
  type: string;
  required: boolean;
  defaultValue?: any;
  description: string;
}

class ComponentAnalyzer {
  parseRequirements(input: string): ComponentSpec {
    // 从用户输入中提取组件规格
    return {
      name: this.extractName(input),
      type: this.inferType(input),
      props: this.extractProps(input),
      state: this.extractState(input),
      hooks: this.identifyHooks(input),
      styling: this.detectStylingApproach(),
      platform: this.detectPlatform(),
    };
  }
}
```

### 2. 生成 React 组件

```typescript
interface GeneratorOptions {
  typescript: boolean;
  testing: boolean;
  storybook: boolean;
  accessibility: boolean;
}

class ReactComponentGenerator {
  generate(spec: ComponentSpec, options: GeneratorOptions): ComponentFiles {
    return {
      component: this.generateComponent(spec, options),
      types: options.typescript ? this.generateTypes(spec) : null,
      styles: this.generateStyles(spec),
      tests: options.testing ? this.generateTests(spec) : null,
      stories: options.storybook ? this.generateStories(spec) : null,
      index: this.generateIndex(spec),
    };
  }

  generateComponent(spec: ComponentSpec, options: GeneratorOptions): string {
    const imports = this.generateImports(spec, options);
    const types = options.typescript ? this.generatePropTypes(spec) : "";
    const component = this.generateComponentBody(spec, options);
    const exports = this.generateExports(spec);

    return `${imports}\n\n${types}\n\n${component}\n\n${exports}`;
  }

  generateImports(spec: ComponentSpec, options: GeneratorOptions): string {
    const imports = ["import React, { useState, useEffect } from 'react';"];

    if (spec.styling === "css-modules") {
      imports.push(`import styles from './${spec.name}.module.css';`);
    } else if (spec.styling === "styled-components") {
      imports.push("import styled from 'styled-components';");
    }

    if (options.accessibility) {
      imports.push("import { useA11y } from '@/hooks/useA11y';");
    }

    return imports.join("\n");
  }

  generatePropTypes(spec: ComponentSpec): string {
    const props = spec.props
      .map((p) => {
        const optional = p.required ? "" : "?";
        const comment = p.description ? `  /** ${p.description} */\n` : "";
        return `${comment}  ${p.name}${optional}: ${p.type};`;
      })
      .join("\n");

    return `export interface ${spec.name}Props {\n${props}\n}`;
  }

  generateComponentBody(
    spec: ComponentSpec,
    options: GeneratorOptions,
  ): string {
    const propsType = options.typescript ? `: React.FC<${spec.name}Props>` : "";
    const destructuredProps = spec.props.map((p) => p.name).join(", ");

    let body = `export const ${spec.name}${propsType} = ({ ${destructuredProps} }) => {\n`;

    // 添加状态 hooks
    if (spec.state) {
      body += spec.state
        .map(
          (s) =>
            `  const [${s.name}, set${this.capitalize(s.name)}] = useState${options.typescript ? `<${s.type}>` : ""}(${s.initial});\n`,
        )
        .join("");
      body += "\n";
    }

    // 添加 effects
    if (spec.hooks?.includes("useEffect")) {
      body += `  useEffect(() => {\n`;
      body += `    // TODO: 添加 effect 逻辑\n`;
      body += `  }, [${destructuredProps}]);\n\n`;
    }

    // 添加可访问性
    if (options.accessibility) {
      body += `  const a11yProps = useA11y({\n`;
      body += `    role: '${this.inferAriaRole(spec.type)}',\n`;
      body += `    label: ${spec.props.find((p) => p.name === "label")?.name || `'${spec.name}'`}\n`;
      body += `  });\n\n`;
    }

    // JSX 返回
    body += `  return (\n`;
    body += this.generateJSX(spec, options);
    body += `  );\n`;
    body += `};`;

    return body;
  }

  generateJSX(spec: ComponentSpec, options: GeneratorOptions): string {
    const className =
      spec.styling === "css-modules"
        ? `className={styles.${this.camelCase(spec.name)}}`
        : "";
    const a11y = options.accessibility ? "{...a11yProps}" : "";

    return (
      `    <div ${className} ${a11y}>\n` +
      `      {/* TODO: 添加组件内容 */}\n` +
      `    </div>\n`
    );
  }
}
```

### 3. 生成 React Native 组件

```typescript
class ReactNativeGenerator {
  generateComponent(spec: ComponentSpec): string {
    return `
import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  AccessibilityInfo
} from 'react-native';

interface ${spec.name}Props {
${spec.props.map((p) => `  ${p.name}${p.required ? "" : "?"}: ${this.mapNativeType(p.type)};`).join("\n")}
}

export const ${spec.name}: React.FC<${spec.name}Props> = ({
  ${spec.props.map((p) => p.name).join(",\n  ")}
}) => {
  return (
    <View
      style={styles.container}
      accessible={true}
      accessibilityLabel="${spec.name} 组件"
    >
      <Text style={styles.text}>
        {/* 组件内容 */}
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
  },
  text: {
    fontSize: 16,
    color: '#333',
  },
});
`;
  }

  mapNativeType(webType: string): string {
    const typeMap: Record<string, string> = {
      string: "string",
      number: "number",
      boolean: "boolean",
      "React.ReactNode": "React.ReactNode",
      Function: "() => void",
    };
    return typeMap[webType] || webType;
  }
}
```

### 4. 生成组件测试

```typescript
class ComponentTestGenerator {
  generateTests(spec: ComponentSpec): string {
    return `
import { render, screen, fireEvent } from '@testing-library/react';
import { ${spec.name} } from './${spec.name}';

describe('${spec.name}', () => {
  const defaultProps = {
${spec.props
  .filter((p) => p.required)
  .map((p) => `    ${p.name}: ${this.getMockValue(p.type)},`)
  .join("\n")}
  };

  it('渲染时不会崩溃', () => {
    render(<${spec.name} {...defaultProps} />);
    expect(screen.getByRole('${this.inferAriaRole(spec.type)}')).toBeInTheDocument();
  });

  it('显示正确的内容', () => {
    render(<${spec.name} {...defaultProps} />);
    expect(screen.getByText(/content/i)).toBeVisible();
  });

${spec.props
  .filter((p) => p.type.includes("()") || p.name.startsWith("on"))
  .map(
    (p) => `
  it('触发时调用 ${p.name}', () => {
    const mock${this.capitalize(p.name)} = jest.fn();
    render(<${spec.name} {...defaultProps} ${p.name}={mock${this.capitalize(p.name)}} />);

    const trigger = screen.getByRole('button');
    fireEvent.click(trigger);

    expect(mock${this.capitalize(p.name)}).toHaveBeenCalledTimes(1);
  });`,
  )
  .join("\n")}

  it('符合可访问性标准', async () => {
    const { container } = render(<${spec.name} {...defaultProps} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
`;
  }

  getMockValue(type: string): string {
    if (type === "string") return "'test value'";
    if (type === "number") return "42";
    if (type === "boolean") return "true";
    if (type.includes("[]")) return "[]";
    if (type.includes("()")) return "jest.fn()";
    return "{}";
  }
}
```

### 5. 生成样式

```typescript
class StyleGenerator {
  generateCSSModule(spec: ComponentSpec): string {
    const className = this.camelCase(spec.name);
    return `
.${className} {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: var(--bg-primary);
}

.${className}Title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.${className}Content {
  flex: 1;
  color: var(--text-secondary);
}
`;
  }

  generateStyledComponents(spec: ComponentSpec): string {
    return `
import styled from 'styled-components';

export const ${spec.name}Container = styled.div\`
  display: flex;
  flex-direction: column;
  padding: \${({ theme }) => theme.spacing.md};
  background-color: \${({ theme }) => theme.colors.background};
\`;

export const ${spec.name}Title = styled.h2\`
  font-size: \${({ theme }) => theme.fontSize.lg};
  font-weight: 600;
  color: \${({ theme }) => theme.colors.text.primary};
  margin-bottom: \${({ theme }) => theme.spacing.sm};
\`;
`;
  }

  generateTailwind(spec: ComponentSpec): string {
    return `
// 在组件中使用这些 Tailwind 类：
// 容器: "flex flex-col p-4 bg-white rounded-lg shadow"
// 标题: "text-xl font-semibold text-gray-900 mb-2"
// 内容: "flex-1 text-gray-700"
`;
  }
}
```

### 6. 生成 Storybook Stories

```typescript
class StorybookGenerator {
  generateStories(spec: ComponentSpec): string {
    return `
import type { Meta, StoryObj } from '@storybook/react';
import { ${spec.name} } from './${spec.name}';

const meta: Meta<typeof ${spec.name}> = {
  title: '组件/${spec.name}',
  component: ${spec.name},
  tags: ['autodocs'],
  argTypes: {
${spec.props.map((p) => `    ${p.name}: { control: '${this.inferControl(p.type)}', description: '${p.description}' },`).join("\n")}
  },
};

export default meta;
type Story = StoryObj<typeof ${spec.name}>;

export const Default: Story = {
  args: {
${spec.props.map((p) => `    ${p.name}: ${p.defaultValue || this.getMockValue(p.type)},`).join("\n")}
  },
};

export const Interactive: Story = {
  args: {
    ...Default.args,
  },
};
`;
  }

  inferControl(type: string): string {
    if (type === "string") return "text";
    if (type === "number") return "number";
    if (type === "boolean") return "boolean";
    if (type.includes("[]")) return "object";
    return "text";
  }
}
```

## 输出格式

1. **组件文件**：完整实现的 React/React Native 组件
2. **类型定义**：TypeScript 接口和类型
3. **样式**：CSS modules、styled-components 或 Tailwind 配置
4. **测试**：完整的测试套件和覆盖
5. **Stories**：用于文档的 Storybook stories
6. **索引文件**：清晰导入的桶导出

专注于创建生产就绪、可访问和可维护的组件，遵循现代 React 模式和最佳实践。
