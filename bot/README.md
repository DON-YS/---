# Telegram Control Layer

The Telegram bot is an administrative control interface.

Security principles:

- administrator allowlist
- no arbitrary shell execution
- explicit confirmation for state-changing operations
- secrets stored outside Git
- Telegram token is never hardcoded
- security tools remain restricted to authorized labs
