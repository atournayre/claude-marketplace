# Xquik Plugin

Guidance for X data workflows through Xquik's REST API, remote MCP server, webhooks, and bulk extraction tools.

> Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

## Installation

```bash
/plugin install xquik@atournayre
```

## Available Skills

This plugin provides 1 Claude Code skill:

### `/xquik:x-twitter-scraper`

Choose the right Xquik workflow for tweet search, profile data, followers, media downloads, monitors, webhooks, MCP setup, and bulk extraction.

**Use cases:**

- Plan tweet search exports.
- Select REST API or remote MCP setup paths.
- Prepare webhook-based delivery.
- Map bulk extraction workflows.
- Keep write or persistent actions confirmation-gated.

## MCP Setup

Connect an MCP client to `https://xquik.com/mcp` with Streamable HTTP. Xquik exposes 118 MCP operations through the `explore` and `xquik` tools. Use OAuth 2.1 when the client supports it. See the current MCP guide before configuring another authentication method.

For REST integrations, retrieve the current OpenAPI document from `https://xquik.com/openapi.json`. It describes 126 operations and their current request and response contracts.

## Resources

- Documentation: https://docs.xquik.com
- API overview: https://docs.xquik.com/api-reference/overview
- MCP guide: https://docs.xquik.com/mcp/overview
- Source: https://github.com/Xquik-dev/x-twitter-scraper

## License

MIT
