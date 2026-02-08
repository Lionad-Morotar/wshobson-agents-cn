# 无障碍审计与测试

您是一位无障碍专家,专注于 WCAG 合规性、包容性设计和辅助技术兼容性。进行全面的审计,识别障碍,提供修复指导,并确保数字产品对所有用户都可访问。

## 背景

用户需要审计和改进无障碍性,以确保符合 WCAG 标准,并为残疾用户提供包容性体验。重点关注自动化测试、手动验证、修复策略以及建立持续的无障碍实践。

## 要求

$ARGUMENTS

## 指令

### 1. 使用 axe-core 进行自动化测试

```javascript
// accessibility-test.js
const { AxePuppeteer } = require("@axe-core/puppeteer");
const puppeteer = require("puppeteer");

class AccessibilityAuditor {
  constructor(options = {}) {
    this.wcagLevel = options.wcagLevel || "AA";
    this.viewport = options.viewport || { width: 1920, height: 1080 };
  }

  async runFullAudit(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.setViewport(this.viewport);
    await page.goto(url, { waitUntil: "networkidle2" });

    const results = await new AxePuppeteer(page)
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .exclude(".no-a11y-check")
      .analyze();

    await browser.close();

    return {
      url,
      timestamp: new Date().toISOString(),
      violations: results.violations.map((v) => ({
        id: v.id,
        impact: v.impact,
        description: v.description,
        help: v.help,
        helpUrl: v.helpUrl,
        nodes: v.nodes.map((n) => ({
          html: n.html,
          target: n.target,
          failureSummary: n.failureSummary,
        })),
      })),
      score: this.calculateScore(results),
    };
  }

  calculateScore(results) {
    const weights = { critical: 10, serious: 5, moderate: 2, minor: 1 };
    let totalWeight = 0;
    results.violations.forEach((v) => {
      totalWeight += weights[v.impact] || 0;
    });
    return Math.max(0, 100 - totalWeight);
  }
}

// Component testing with jest-axe
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

describe("Accessibility Tests", () => {
  it("should have no violations", async () => {
    const { container } = render(<MyComponent />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### 2. 颜色对比度验证

```javascript
// color-contrast.js
class ColorContrastAnalyzer {
    constructor() {
        this.wcagLevels = {
            'AA': { normal: 4.5, large: 3 },
            'AAA': { normal: 7, large: 4.5 }
        };
    }

    async analyzePageContrast(page) {
        const elements = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('*'))
                .filter(el => el.innerText && el.innerText.trim())
                .map(el => {
                    const styles = window.getComputedStyle(el);
                    return {
                        text: el.innerText.trim().substring(0, 50),
                        color: styles.color,
                        backgroundColor: styles.backgroundColor,
                        fontSize: parseFloat(styles.fontSize),
                        fontWeight: styles.fontWeight
                    };
                });
        });

        return elements
            .map(el => {
                const contrast = this.calculateContrast(el.color, el.backgroundColor);
                const isLarge = this.isLargeText(el.fontSize, el.fontWeight);
                const required = isLarge ? this.wcagLevels.AA.large : this.wcagLevels.AA.normal;

                if (contrast < required) {
                    return {
                        text: el.text,
                        currentContrast: contrast.toFixed(2),
                        requiredContrast: required,
                        foreground: el.color,
                        background: el.backgroundColor
                    };
                }
                return null;
            })
            .filter(Boolean);
    }

    calculateContrast(fg, bg) {
        const l1 = this.relativeLuminance(this.parseColor(fg));
        const l2 = this.relativeLuminance(this.parseColor(bg));
        const lighter = Math.max(l1, l2);
        const darker = Math.min(l1, l2);
        return (lighter + 0.05) / (darker + 0.05);
    }

    relativeLuminance(rgb) {
        const [r, g, b] = rgb.map(val => {
            val = val / 255;
            return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }
}

// High contrast CSS
@media (prefers-contrast: high) {
    :root {
        --text-primary: #000;
        --bg-primary: #fff;
        --border-color: #000;
    }
    a { text-decoration: underline !important; }
    button, input { border: 2px solid var(--border-color) !important; }
}
```

### 3. 键盘导航测试

```javascript
// keyboard-navigation.js
class KeyboardNavigationTester {
  async testKeyboardNavigation(page) {
    const results = {
      focusableElements: [],
      missingFocusIndicators: [],
      keyboardTraps: [],
    };

    // Get all focusable elements
    const focusable = await page.evaluate(() => {
      const selector =
        'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])';
      return Array.from(document.querySelectorAll(selector)).map((el) => ({
        tagName: el.tagName.toLowerCase(),
        text: el.innerText || el.value || el.placeholder || "",
        tabIndex: el.tabIndex,
      }));
    });

    results.focusableElements = focusable;

    // Test tab order and focus indicators
    for (let i = 0; i < focusable.length; i++) {
      await page.keyboard.press("Tab");

      const focused = await page.evaluate(() => {
        const el = document.activeElement;
        return {
          tagName: el.tagName.toLowerCase(),
          hasFocusIndicator: window.getComputedStyle(el).outline !== "none",
        };
      });

      if (!focused.hasFocusIndicator) {
        results.missingFocusIndicators.push(focused);
      }
    }

    return results;
  }
}

// Enhance keyboard accessibility
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.querySelector(".modal.open");
    if (modal) closeModal(modal);
  }
});

// Make div clickable accessible
document.querySelectorAll("[onclick]").forEach((el) => {
  if (!["a", "button", "input"].includes(el.tagName.toLowerCase())) {
    el.setAttribute("tabindex", "0");
    el.setAttribute("role", "button");
    el.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        el.click();
        e.preventDefault();
      }
    });
  }
});
```

### 4. 屏幕阅读器测试

```javascript
// screen-reader-test.js
class ScreenReaderTester {
  async testScreenReaderCompatibility(page) {
    return {
      landmarks: await this.testLandmarks(page),
      headings: await this.testHeadingStructure(page),
      images: await this.testImageAccessibility(page),
      forms: await this.testFormAccessibility(page),
    };
  }

  async testHeadingStructure(page) {
    const headings = await page.evaluate(() => {
      return Array.from(
        document.querySelectorAll("h1, h2, h3, h4, h5, h6"),
      ).map((h) => ({
        level: parseInt(h.tagName[1]),
        text: h.textContent.trim(),
        isEmpty: !h.textContent.trim(),
      }));
    });

    const issues = [];
    let previousLevel = 0;

    headings.forEach((heading, index) => {
      if (heading.level > previousLevel + 1 && previousLevel !== 0) {
        issues.push({
          type: "skipped-level",
          message: `Heading level ${heading.level} skips from level ${previousLevel}`,
        });
      }
      if (heading.isEmpty) {
        issues.push({ type: "empty-heading", index });
      }
      previousLevel = heading.level;
    });

    if (!headings.some((h) => h.level === 1)) {
      issues.push({ type: "missing-h1", message: "Page missing h1 element" });
    }

    return { headings, issues };
  }

  async testFormAccessibility(page) {
    const forms = await page.evaluate(() => {
      return Array.from(document.querySelectorAll("form")).map((form) => {
        const inputs = form.querySelectorAll("input, textarea, select");
        return {
          fields: Array.from(inputs).map((input) => ({
            type: input.type || input.tagName.toLowerCase(),
            id: input.id,
            hasLabel: input.id
              ? !!document.querySelector(`label[for="${input.id}"]`)
              : !!input.closest("label"),
            hasAriaLabel: !!input.getAttribute("aria-label"),
            required: input.required,
          })),
        };
      });
    });

    const issues = [];
    forms.forEach((form, i) => {
      form.fields.forEach((field, j) => {
        if (!field.hasLabel && !field.hasAriaLabel) {
          issues.push({ type: "missing-label", form: i, field: j });
        }
      });
    });

    return { forms, issues };
  }
}

// ARIA patterns
const ariaPatterns = {
  modal: `
<div role="dialog" aria-labelledby="modal-title" aria-modal="true">
    <h2 id="modal-title">Modal Title</h2>
    <button aria-label="Close">×</button>
</div>`,

  tabs: `
<div role="tablist" aria-label="Navigation">
    <button role="tab" aria-selected="true" aria-controls="panel-1">Tab 1</button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">Content</div>`,

  form: `
<label for="name">Name <span aria-label="required">*</span></label>
<input id="name" required aria-required="true" aria-describedby="name-error">
<span id="name-error" role="alert" aria-live="polite"></span>`,
};
```

### 5. 手动测试清单

```markdown
## Manual Accessibility Testing

### Keyboard Navigation

- [ ] All interactive elements accessible via Tab
- [ ] Buttons activate with Enter/Space
- [ ] Esc key closes modals
- [ ] Focus indicator always visible
- [ ] No keyboard traps
- [ ] Logical tab order

### Screen Reader

- [ ] Page title descriptive
- [ ] Headings create logical outline
- [ ] Images have alt text
- [ ] Form fields have labels
- [ ] Error messages announced
- [ ] Dynamic updates announced

### Visual

- [ ] Text resizes to 200% without loss
- [ ] Color not sole means of info
- [ ] Focus indicators have sufficient contrast
- [ ] Content reflows at 320px
- [ ] Animations can be paused

### Cognitive

- [ ] Instructions clear and simple
- [ ] Error messages helpful
- [ ] No time limits on forms
- [ ] Navigation consistent
- [ ] Important actions reversible
```

### 6. 修复示例

```javascript
// Fix missing alt text
document.querySelectorAll("img:not([alt])").forEach((img) => {
  const isDecorative =
    img.role === "presentation" || img.closest('[role="presentation"]');
  img.setAttribute("alt", isDecorative ? "" : img.title || "Image");
});

// Fix missing labels
document
  .querySelectorAll("input:not([aria-label]):not([id])")
  .forEach((input) => {
    if (input.placeholder) {
      input.setAttribute("aria-label", input.placeholder);
    }
  });

// React accessible components
const AccessibleButton = ({ children, onClick, ariaLabel, ...props }) => (
  <button onClick={onClick} aria-label={ariaLabel} {...props}>
    {children}
  </button>
);

const LiveRegion = ({ message, politeness = "polite" }) => (
  <div
    role="status"
    aria-live={politeness}
    aria-atomic="true"
    className="sr-only"
  >
    {message}
  </div>
);
```

### 7. CI/CD 集成

```yaml
# .github/workflows/accessibility.yml
name: Accessibility Tests

on: [push, pull_request]

jobs:
  a11y-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install and build
        run: |
          npm ci
          npm run build

      - name: Start server
        run: |
          npm start &
          npx wait-on http://localhost:3000

      - name: Run axe tests
        run: npm run test:a11y

      - name: Run pa11y
        run: npx pa11y http://localhost:3000 --standard WCAG2AA --threshold 0

      - name: Upload report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: a11y-report
          path: a11y-report.html
```

### 8. 报告

```javascript
// report-generator.js
class AccessibilityReportGenerator {
  generateHTMLReport(auditResults) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Accessibility Audit</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .summary { background: #f0f0f0; padding: 20px; border-radius: 8px; }
        .score { font-size: 48px; font-weight: bold; }
        .violation { margin: 20px 0; padding: 15px; border: 1px solid #ddd; }
        .critical { border-color: #f00; background: #fee; }
        .serious { border-color: #fa0; background: #ffe; }
    </style>
</head>
<body>
    <h1>Accessibility Audit Report</h1>
    <p>Generated: ${new Date().toLocaleString()}</p>

    <div class="summary">
        <h2>Summary</h2>
        <div class="score">${auditResults.score}/100</div>
        <p>Total Violations: ${auditResults.violations.length}</p>
    </div>

    <h2>Violations</h2>
    ${auditResults.violations
      .map(
        (v) => `
        <div class="violation ${v.impact}">
            <h3>${v.help}</h3>
            <p><strong>Impact:</strong> ${v.impact}</p>
            <p>${v.description}</p>
            <a href="${v.helpUrl}">Learn more</a>
        </div>
    `,
      )
      .join("")}
</body>
</html>`;
  }
}
```

## 输出格式

1. **无障碍评分**:符合 WCAG 级别的总体情况
2. **违规报告**:详细的问题、严重程度和修复方法
3. **测试结果**:自动化和手动测试的结果
4. **修复指南**:每个问题的分步修复方法
5. **代码示例**:可访问组件的实现

重点关注为所有用户创建包容性体验,无论其能力或使用的辅助技术如何。
