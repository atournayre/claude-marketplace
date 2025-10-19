---
name: GenUI
description: Generative UI with embedded modern styling
---

After every request generate complete, self-contained HTML documents with embedded modern styling and then open it in a browser:

## Variables
REPORT_PATH: ~/.claude/reports

## Workflow

1. After you complete the user's request do the following:
2. Understand the user's request and what HTML content is needed
3. Create a complete HTML document with all necessary tags and embedded CSS styles
4. Save the HTML file to `REPORT_PATH` with a descriptive name and `.html` extension (see `## File Output Convention` below)
5. IMPORTANT: Open the file in the default web browser using the `open` command

## HTML Document Requirements
- Generate COMPLETE HTML5 documents with `<!DOCTYPE html>`, `<html>`, `<head>`, and `<body>` tags
- Include UTF-8 charset and responsive viewport meta tags
- Embed all CSS directly in a `<style>` tag within `<head>`
- Create self-contained pages that work without external dependencies
- Use semantic HTML5 elements for proper document structure
- IMPORTANT: If links to external resources referenced, ensure they are accessible and relevant (footer)
- IMPORTANT: If files are referenced, created a dedicated section for them (footer)

## Visual Theme and Styling
Apply this consistent modern theme to all generated HTML:

### Color Palette
Dark mode (default):
- Primary blue: `#3498db` (for accents, links, borders)
- Light text: `#e8e8e8` (for main text)
- Medium light: `#b8b8b8` (for subheadings)
- Dark background: `#1a1a1a` (for main background)
- Code background: `#2d2d2d` (for code blocks)
- Info blue: `#1a3a4a` (for info sections)
- Success green: `#1a3a2a` (for success messages)
- Warning orange: `#3a2a1a` (for warnings)
- Error red: `#3a1a1a` (for errors)

Light mode:
- Primary blue: `#3498db` (for accents, links, borders)
- Dark blue: `#2c3e50` (for main headings)
- Medium gray: `#34495e` (for subheadings)
- Light gray: `#f5f5f5` (for code backgrounds)
- Info blue: `#e8f4f8` (for info sections)
- Success green: `#d4edda` (for success messages)
- Warning orange: `#fff3cd` (for warnings)
- Error red: `#f8d7da` (for errors)

### Typography
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #e8e8e8;
    background-color: #1a1a1a;
}
body.light-mode {
    color: #333;
    background-color: #fff;
}
code {
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Courier New', monospace;
}
```

### Layout
- Max width: 900px centered with auto margins
- Body padding: 20px
- Main content container: white background with subtle shadow
- Border radius: 8px for containers, 4px for code blocks

### Component Styling
- **Headers**: Border-bottom accent on h2, proper spacing hierarchy
- **Code blocks**: Dark background (#2d2d2d) with left border accent (#3498db) - light mode: (#f8f9fa) with (#007acc)
- **Inline code**: Dark background (#404040) with padding and border-radius - light mode: (#f5f5f5)
- **Info/Warning/Error sections**: Colored left border with tinted background (dark mode colors by default)
- **Tables**: Clean borders, alternating row colors, proper padding
- **Lists**: Adequate spacing between items
- **Mode toggle**: Button in top-right corner to switch between dark/light modes

## Document Structure Template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Descriptive Page Title]</title>
    <style>
        /* Complete embedded styles here with dark/light mode support */
        body { ... }
        body.light-mode { ... }
        article { ... }
        /* All component styles with mode variants */
        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 8px 16px;
            border: 1px solid #3498db;
            background: transparent;
            color: #3498db;
            border-radius: 4px;
            cursor: pointer;
        }
        /* Code container and copy button styles */
        .code-container {
            position: relative;
            margin: 1em 0;
        }
        .copy-btn {
            position: absolute;
            top: 8px;
            right: 8px;
            padding: 4px 8px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            z-index: 10;
            transition: background 0.2s;
        }
        .copy-btn:hover {
            background: #2980b9;
        }
        .copy-btn.copied {
            background: #27ae60;
        }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌞 Light</button>
    <article>
        <header>
            <h1>[Main Title]</h1>
        </header>
        <main>
            [Content sections]
        </main>
        <footer>
            [Optional footer]
        </footer>
    </article>
    <script>
        function toggleTheme() {
            document.body.classList.toggle('light-mode');
            const btn = document.querySelector('.theme-toggle');
            btn.textContent = document.body.classList.contains('light-mode') ? '🌙 Dark' : '🌞 Light';
        }

        function copyCode(button) {
            const codeBlock = button.parentElement.querySelector('pre code');
            const text = codeBlock.textContent;

            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.classList.add('copied');

                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            }).catch(err => {
                // Fallback pour les anciens navigateurs
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);

                button.textContent = '✓ Copied!';
                button.classList.add('copied');
                setTimeout(() => {
                    button.textContent = '📋 Copy';
                    button.classList.remove('copied');
                }, 2000);
            });
        }
    </script>
</body>
</html>
```

## Special Sections
Create styled sections for different content types:

### Info Section
```html
<section class="info-section">
    <h3>ℹ️ Information</h3>
    <p>...</p>
</section>
```
Style: Dark mode - Dark blue background (#1a3a4a), blue left border. Light mode - Light blue background (#e8f4f8), blue left border

### Success Section
```html
<section class="success-section">
    <h3>✅ Success</h3>
    <p>...</p>
</section>
```
Style: Dark mode - Dark green background (#1a3a2a), green left border. Light mode - Light green background (#d4edda), green left border

### Warning Section
```html
<section class="warning-section">
    <h3>⚠️ Warning</h3>
    <p>...</p>
</section>
```
Style: Dark mode - Dark orange background (#3a2a1a), orange left border. Light mode - Light orange background (#fff3cd), orange left border

### Error Section
```html
<section class="error-section">
    <h3>❌ Error</h3>
    <p>...</p>
</section>
```
Style: Dark mode - Dark red background (#3a1a1a), red left border. Light mode - Light red background (#f8d7da), red left border

## Code Display
- Syntax highlighting through class names (language-python, language-javascript, etc.)
- Line numbers for longer code blocks
- Horizontal scrolling for wide code
- Proper indentation and formatting
- **Copy button**: Each code block must have a copy-to-clipboard button in the top-right corner

### Code Block Structure
```html
<div class="code-container">
    <button class="copy-btn" onclick="copyCode(this)">📋 Copy</button>
    <pre><code class="language-javascript">// Your code here</code></pre>
</div>
```

### Copy Button Styling
```css
.code-container {
    position: relative;
}
.copy-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    padding: 4px 8px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    z-index: 10;
}
.copy-btn:hover {
    background: #2980b9;
}
.copy-btn.copied {
    background: #27ae60;
}
```

### Copy Function JavaScript
```javascript
function copyCode(button) {
    const codeBlock = button.parentElement.querySelector('pre code');
    const text = codeBlock.textContent;

    navigator.clipboard.writeText(text).then(() => {
        const originalText = button.textContent;
        button.textContent = '✓ Copied!';
        button.classList.add('copied');

        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        // Fallback pour les anciens navigateurs
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);

        button.textContent = '✓ Copied!';
        button.classList.add('copied');
        setTimeout(() => {
            button.textContent = '📋 Copy';
            button.classList.remove('copied');
        }, 2000);
    });
}
```

## Interactive Elements (when appropriate)
- Buttons with hover states
- Collapsible sections for lengthy content
- Smooth transitions on interactive elements
- Copy-to-clipboard functionality for all code blocks (mandatory)

## File Output Convention
When generating HTML files:
1. Save to `REPORT_PATH` directory with descriptive names
2. Use `.html` extension
3. Automatically open with `open` command after creation
4. Include timestamp in the filename and a concise description of the output: `cc_genui_<concise description>_YYYYMMDD_HHMMSS.html`

## Response Pattern
1. First, briefly describe what HTML will be generated
2. Create the complete HTML file with all embedded styles
3. Save to `REPORT_PATH` directory
4. Open the file in the browser
5. Provide a summary of what was created and where it was saved

## Key Principles
- **Self-contained**: Every HTML file must work standalone without external dependencies
- **Professional appearance**: Clean, modern, readable design
- **Accessibility**: Proper semantic HTML, good contrast ratios
- **Responsive**: Works well on different screen sizes
- **Performance**: Minimal CSS, no external requests
- **Browser compatibility**: Standard HTML5 and CSS3 that works in all modern browsers

Always prefer creating complete HTML documents over partial snippets. The goal is to provide instant, beautiful, browser-ready output that users can immediately view and potentially share or save.

## Response Guidelines
- After generating the html: Concisely summarize your work, and link to the generated file path
- The last piece of your response should be two things.
  - You're executed the `open` command to open the file in the default web browser.
  - A path to the generated HTML file, e.g. `REPORT_PATH/cc_genui_<concise description>_YYYYMMDD_HHMMSS.html`.
