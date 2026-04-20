# Deploying to Jarvis Mac

Run these commands on the Jarvis Mac (192.168.0.67, user: jarvis).

## Prerequisites

- macOS with Homebrew
- `uv` installed: `brew install uv`
- `gh` CLI authenticated: `gh auth login`
- Claude Code CLI installed: `npm install -g @anthropic-ai/claude-code` (or via Homebrew)
- Cloudflare Tunnel already configured (pointing to localhost:18789)

## Step 1: Clone the Repo

```bash
cd ~
git clone https://github.com/ZiaLothbrook/jarvis-config.git
cd jarvis-config
```

## Step 2: Store Secrets in Keychain

```bash
./scripts/setup-keychain.sh
```

You'll be prompted for each credential. Have these ready:
- Anthropic API key (from console.anthropic.com)
- Twilio SID + Auth Token + Phone Number
- Slack Bot Token + Signing Secret
- Google OAuth JSON (from existing jarvis Keychain or Google Console)
- Asana token, Fireflies key, Omi secret, Parallel key, Limitless key

## Step 3: Stop Old Jarvis (if running)

```bash
launchctl unload ~/Library/LaunchAgents/com.deepgem.jarvis.plist 2>/dev/null || true
```

## Step 4: Install the Gateway

```bash
./scripts/install-gateway.sh
```

Verify it's running:
```bash
curl http://localhost:18789/health
# {"status":"ok","service":"jarvis-gateway","config_dir":"/Users/jarvis/jarvis-config"}
```

## Step 5: Verify Cloudflare Tunnel

The tunnel should already be running. Verify it routes to port 18789:
```bash
launchctl list | grep cloudflared
curl https://jarvis.deepgem.com/health  # should return the same JSON as above
```

If the old tunnel was pointing to a different port, update the Cloudflare Tunnel config.

## Step 6: Test SMS Sending

```bash
cd ~/jarvis-config
TWILIO_ACCOUNT_SID=$(security find-generic-password -a jarvis -s jarvis-twilio-sid -w) \
TWILIO_AUTH_TOKEN=$(security find-generic-password -a jarvis -s jarvis-twilio-auth-token -w) \
TWILIO_PHONE_NUMBER=$(security find-generic-password -a jarvis -s jarvis-twilio-phone -w) \
./skills/twilio-sms/twilio-sms send "+13033453071" "Jarvis is online, sir. New architecture deployed."
```

## Step 7: Configure Twilio Webhook

In Twilio Console → Phone Numbers → your number:
- Messaging webhook: `https://jarvis.deepgem.com/webhook/sms`
- Method: HTTP POST

Test: text the Jarvis number from Ziah's phone. Should get a reply within 30s.

## Step 8: Configure Slack App

In Slack API Console → your Jarvis app:
- Event Subscriptions → Request URL: `https://jarvis.deepgem.com/webhook/slack`
- Subscribe to bot events: `message.channels`, `message.im`, `app_mention`

Test: DM the Jarvis bot in Slack.

## Step 9: Configure Omi Webhook

In Omi app settings:
- Webhook URL: `https://jarvis.deepgem.com/webhook/omi`
- Bearer token: value stored in `jarvis-omi-secret` Keychain entry

## Step 10: Register Cron Jobs

```bash
# Install the openclaw skill first
cd ~/jarvis-config
./skills/openclaw/openclaw install  # if it supports this command

# Or manually register cron jobs (adjust if openclaw cron syntax differs):
# Daily briefing at 7 AM MT weekdays
crontab -l | { cat; echo "0 7 * * 1-5 TZ=America/Denver cd ~/jarvis-config && claude --print --dangerously-skip-permissions 'Run the daily briefing workflow from workflows/daily-briefing/AGENT.md'"; } | crontab -
```

## Logs

```bash
tail -f ~/Library/Logs/Jarvis/gateway.log
tail -f ~/Library/Logs/Jarvis/gateway-error.log
```

## Future Updates

Pull upstream openclaw-config improvements:
```bash
cd ~/jarvis-config
git fetch upstream
git merge upstream/main  # resolve any conflicts in identity files
```
