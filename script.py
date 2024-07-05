import os
import discord
import asyncio
import time
from discord.ext import commands
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

TOKEN = 'Enter Your Token'
CHANNEL_ID = 'Enter your Channel ID'
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, loop):
        self.loop = loop
        self.processed_files = set()
        self.last_modified = {}

    def on_created(self, event):
        if not event.is_directory and not os.path.basename(event.src_path).startswith('.'):
            print(f"New screenshot detected: {event.src_path}")
            self.last_modified[event.src_path] = time.time()
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self.process_file(event.src_path)
            )

    def on_modified(self, event):
        if not event.is_directory and not os.path.basename(event.src_path).startswith('.'):
            print(f"File modified: {event.src_path}")
            self.last_modified[event.src_path] = time.time()
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self.process_file(event.src_path)
            )

    async def process_file(self, file_path):
        await bot.wait_until_ready()
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            try:
                # Debounce logic to ensure the file is fully written and not reprocessed immediately
                while True:
                    await asyncio.sleep(2)  # Wait 2 seconds
                    last_mod_time = self.last_modified.get(file_path, 0)
                    if time.time() - last_mod_time >= 2:
                        break

                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    return

                if file_path not in self.processed_files:
                    self.processed_files.add(file_path)
                    print(f"Uploading file: {file_path}")
                    await channel.send(file=discord.File(file_path))
                    print(f"File uploaded: {file_path}")
            except discord.errors.HTTPException as e:
                print(f"Failed to send file: {e}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
        else:
            print("Channel not found. Please check if the CHANNEL_ID is correct.")

async def setup_watcher(path, loop):
    event_handler = ScreenshotHandler(loop)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        await asyncio.Event().wait()
    finally:
        observer.stop()
        observer.join()

async def run_bot():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(f"Bot encountered an error: {e}")
        await bot.close()

async def main():
    screenshot_path = '/Users/aarongurovich/Desktop'
    loop = asyncio.get_running_loop()
    watcher_task = asyncio.create_task(setup_watcher(screenshot_path, loop))

    while True:
        try:
            await run_bot()
        except Exception as e:
            print(f"Bot loop encountered an error: {e}")
            await asyncio.sleep(5)  # Wait before retrying
        finally:
            if not watcher_task.done():
                watcher_task.cancel()
                try:
                    await watcher_task
                except asyncio.CancelledError:
                    pass

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

if __name__ == "__main__":
    asyncio.run(main())
