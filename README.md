## Discord SMM

A fully automatic token joiner for discord using oAuth2 workflow.

## Features

- Sellix integration with custom amounts<br>
- Auto removes non working auths<br>
- Auto skips already in tokens within 1 minute depending on the server size before continuing with joining.<br>
- Logs every event on webhook ( completion, errors etc. with detailed information )<br>
- A bot to create keys manually and track running orders<br>
- Advanced error handelling, attempts to serve flawless joining.<br>
- Multi Threaded, Can join in multiple servers at the same time concurrently.

## Usage

1. Create a new application at https://canary.discord.com/developers/applications<br>
2. Authorize tokens to your bot, auths must be in format user_id:auth_token:refresh_token<br>
3. Add auths in offline.txt or online.txt depending on the type.<br>
4. Configure bot's client id, client secret, webhook and your server url followed by /callback in config.json<br>
5. Run python main.py<br>
6. Run python webhook.py for sellix integration if required, add its url in dynamic section of sellix.
