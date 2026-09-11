import asyncio
import os
import socket
import ssl
from io import BytesIO

import aiohttp
import discord
from discord.ext.commands import Cog

from src.bot import Shinchan


class Ssverification(Cog):
    def __init__(self, bot: Shinchan):
        self.bot = bot

        self.fastapi_url = os.getenv(
            "FASTAPI_URL",
            getattr(self.bot.config, "FASTAPI_URL", "")
        ).strip().rstrip("/")

        self.request_url = (
            f"{self.fastapi_url}/ocr"
            if self.fastapi_url
            else ""
        )

        self.headers = {
            "authorization": os.getenv(
                "FASTAPI_KEY",
                getattr(self.bot.config, "FASTAPI_KEY", "")
            ),
            "Content-Type": "application/json",
        }

        self.__verify_lock = asyncio.Lock()

    async def _ocr_request(self, data):
        """
        Normal OCR request.
        If the OCR server has an SNI/TLS problem, retry using
        the resolved IP while preserving the original Host header.
        """

        timeout = aiohttp.ClientTimeout(total=45)

        try:
            async with self.bot.session.post(
                self.request_url,
                json=data,
                headers=self.headers,
                timeout=timeout,
            ) as resp:
                return await resp.json()

        except aiohttp.ClientConnectorSSLError:
            # SSL/SNI fallback
            try:
                hostname = socket.gethostbyname(
                    self.fastapi_url.split("://", 1)[-1].split("/", 1)[0]
                )

                original_host = (
                    self.fastapi_url
                    .split("://", 1)[-1]
                    .split("/", 1)[0]
                )

                fallback_url = f"https://{hostname}/ocr"

                unsafe_ssl = ssl.create_default_context()
                unsafe_ssl.check_hostname = False
                unsafe_ssl.verify_mode = ssl.CERT_NONE

                fallback_headers = dict(self.headers)
                fallback_headers["Host"] = original_host

                async with self.bot.session.post(
                    fallback_url,
                    json=data,
                    headers=fallback_headers,
                    timeout=timeout,
                    ssl=unsafe_ssl,
                ) as resp:
                    return await resp.json()

            except Exception as exc:
                print(
                    f"[SSVERIFY] SSL fallback failed: "
                    f"{type(exc).__name__}: {exc}"
                )
                raise

    @Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignore bots
        if message.author.bot:
            return

        # No attachments
        if not message.attachments:
            return

        # Only process image attachments
        image_attachments = [
            attachment
            for attachment in message.attachments
            if attachment.content_type
            and attachment.content_type.startswith("image/")
        ]

        if not image_attachments:
            return

        # OCR endpoint missing
        if not self.request_url:
            try:
                await message.channel.send(
                    "❌ SS verification is not configured."
                )
            except Exception:
                pass
            return

        loading_message = None

        try:
            loading_message = await message.channel.send(
                f"Processing your {len(image_attachments)} "
                f"screenshot{'s' if len(image_attachments) != 1 else ''}... loading"
            )

            async with self.__verify_lock:

                results = []

                for attachment in image_attachments:

                    try:
                        image_bytes = await attachment.read()

                        _data = {
                            "image": image_bytes.hex()
                        }

                        _ocr = await self._ocr_request(_data)

                        if not isinstance(_ocr, list):
                            print(
                                "[SSVERIFY] OCR server returned "
                                "an unexpected response."
                            )
                            continue

                        results.extend(_ocr)

                    except (
                        aiohttp.ClientError,
                        asyncio.TimeoutError,
                        OSError,
                        ValueError,
                    ) as exc:

                        print(
                            f"[SSVERIFY] OCR request failed: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        continue

                # Nothing could be verified
                if not results:

                    try:
                        await loading_message.edit(
                            content=(
                                "❌ **SS Verification temporarily unavailable.**\n"
                                "The OCR verification server could not be reached. "
                                "Please try again later."
                            )
                        )
                    except Exception:
                        pass

                    return

                # Process OCR results
                verified = []

                for result in results:

                    if not isinstance(result, dict):
                        continue

                    verified.append(result)

                if not verified:

                    try:
                        await loading_message.edit(
                            content=(
                                "❌ **No valid screenshot data was detected.**"
                            )
                        )
                    except Exception:
                        pass

                    return

                # Build result text
                lines = [
                    "✅ **Screenshot verification completed.**",
                    "",
                ]

                for index, result in enumerate(verified, start=1):

                    lines.append(
                        f"**Screenshot {index}:**"
                    )

                    for key, value in result.items():

                        if value is None:
                            continue

                        lines.append(
                            f"• **{str(key).replace('_', ' ').title()}:** "
                            f"{value}"
                        )

                    lines.append("")

                result_text = "\n".join(lines)

                # Discord message limit protection
                if len(result_text) > 1900:
                    result_text = result_text[:1890] + "\n..."

                try:
                    await loading_message.edit(
                        content=result_text
                    )
                except Exception as exc:
                    print(
                        f"[SSVERIFY] Failed to edit result message: "
                        f"{type(exc).__name__}: {exc}"
                    )

        except Exception as exc:

            print(
                f"[SSVERIFY] Unexpected error: "
                f"{type(exc).__name__}: {exc}"
            )

            if loading_message:

                try:
                    await loading_message.edit(
                        content=(
                            "❌ **SS Verification failed.**\n"
                            "Please try again later."
                        )
                    )
                except Exception:
                    pass


async def setup(bot: Shinchan):
    await bot.add_cog(Ssverification(bot))
