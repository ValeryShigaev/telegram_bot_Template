<h1>telegram_bot_Template</h1>
Aiogram + Fastapi on Nginx and Postgres backend + Docker
<br>
<br>
This is a template for creating a telegram bot that uses a fastapi and postgres backend.
<br>

<h2>Dependencies</h2>

<ul>
<li>FastApi 0.110.0</li>
<li>Postgres 15.2</li>
<li>Aiogram 3.13.1</li>
<li>Redis 5.0.3</li>
<li>Nginx 1.27.2</li>
</ul>

<h2>Services (containers)</h2>

<ul>
<li>Api - contains an API with simple authorization and a test endpoint</li>
<li>DB - contains a postgres database, in the conf/db/scripts folder there is a script for creating a schema and a test user with login: admin@admin.com password: admin</li>
<li>Nginx - enables Nginx and forwards to API port</li>
<li>Bot - contains a bot in which pre-authorization in the API is configured and access to the test endpoint using the start command</li>
<li>Redis - redis storage</li>
</ul>

<h2>Installation</h2>

<ol>
<li>Go to root and rename .env.example to .env then set your parameters especially to the bot token</li>
<li>Make sure that ports 80, 5432, 5000, 6379 are not busy</li>
<li>Launch <code>docker-compose up --build (-d)</code></li>
</ol>