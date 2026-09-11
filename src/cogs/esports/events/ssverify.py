import asyncio
import os
import socket
import ssl
from io import BytesIO

import aiohttp
import discord
from discord.ext.commands import Cog


class Ssverification(Cog):
    def __init__(self, bot):
        self.bot = bot

        # OCR API URL
        self.fastapi_url = os.getenv(
            "FASTAPI_URL",
            getattr(self.bot.config, "FASTAPI_URL", "")
        ).strip().rstrip("/")

        self.request_url = (
            f"{self.fastapi_url}/ocr"
            if self.fastapi_url
            else ""
        )

        # OCR API Key
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
        Send screenshot to OCR API.
        Includes SSL/SNI fallback for problematic OCR servers.
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
                hostname = self.fastapi_url.split(
                    "://", 1
                )[-1].split("/", 1)[0]

                resolved_ip = socket.gethostbyname(hostname)

                fallback_url = (
                    f"https://{resolved_ip}/ocr"
                )

                fallback_headers = dict(self.headers)

                # Keep original hostname for virtual-host routing
                fallback_headers["Host"] = hostname

                unsafe_ssl = ssl.create_default_context()

                unsafe_ssl.check_hostname = False
                unsafe_ssl.verify_mode = ssl.CERT_NONE

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
                    "[SSVERIFY] SSL fallback failed: "
                    f"{type(exc).__name__}: {exc}"
                )

                raise

    async def _send_loading_message(self, message, count):
        try:
            return await message.channel.send(
                f"Processing your {count} "
                f"screenshot{'s' if count != 1 else ''}... loading"
            )

        except Exception as exc:
            print(
                "[SSVERIFY] Failed to send loading message: "
                f"{type(exc).__name__}: {exc}"
            )

            return None

    async def _edit_message(self, message, content):
        if not message:
            return

        try:
            await message.edit(content=content)

        except Exception as exc:
            print(
                "[SSVERIFY] Failed to edit message: "
                f"{type(exc).__name__}: {exc}"
            )

    @Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignore bot messages
        if message.author.bot:
            return

        # No attachments
        if not message.attachments:
            return

        # Only images
        image_attachments = [
            attachment
            for attachment in message.attachments
            if (
                attachment.content_type
                and attachment.content_type.startswith("image/")
            )
        ]

        if not image_attachments:
            return

        # OCR API configuration check
        if not self.request_url:

            await self._edit_message(
                await self._send_loading_message(
                    message,
                    len(image_attachments)
                ),
                "❌ **SS Verification is not configured.**"
            )

            return

        loading_message = await self._send_loading_message(
            message,
            len(image_attachments)
        )

        if not loading_message:
            return

        try:

            async with self.__verify_lock:

                results = []

                for attachment in image_attachments:

                    try:
                        # Download screenshot
                        image_bytes = await attachment.read()

                        # Convert image to hex
                        image_hex = image_bytes.hex()

                        data = {
                            "image": image_hex
                        }

                        # Send to OCR API
                        ocr_result = await self._ocr_request(
                            data
                        )

                        if not isinstance(ocr_result, list):
                            print(
                                "[SSVERIFY] OCR API returned "
                                "an unexpected response."
                            )

                            continue

                        results.extend(ocr_result)

                    except aiohttp.ClientConnectorSSLError as exc:

                        print(
                            "[SSVERIFY] SSL error: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        continue

                    except aiohttp.ClientError as exc:

                        print(
                            "[SSVERIFY] HTTP error: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        continue

                    except asyncio.TimeoutError:

                        print(
                            "[SSVERIFY] OCR request timed out."
                        )

                        continue

                    except OSError as exc:

                        print(
                            "[SSVERIFY] OS error: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        continue

                    except ValueError as exc:

                        print(
                            "[SSVERIFY] Invalid OCR response: "
                            f"{exc}"
                        )

                        continue

                    except Exception as exc:

                        print(
                            "[SSVERIFY] Screenshot processing error: "
                            f"{type(exc).__name__}: {exc}"
                        )

                        continue

                # Nothing returned from OCR
                if not results:

                    await self._edit_message(
                        loading_message,
                        (
                            "❌ **SS Verification temporarily unavailable.**\n"
                            "The OCR verification server could not be reached.\n"
                            "Please try again later."
                        )
                    )

                    return

                # Validate results
                valid_results = [
                    result
                    for result in results
                    if isinstance(result, dict)
                ]

                if not valid_results:

                    await self._edit_message(
                        loading_message,
                        (
                            "❌ **No valid screenshot data was detected.**\n"
                            "Please upload a clear screenshot and try again."
                        )
                    )

                    return

                # Build result
                lines = [
                    "✅ **Screenshot verification completed.**",
                    ""
                ]

                for index, result in enumerate(
                    valid_results,
                    start=1
                ):

                    lines.append(
                        f"**Screenshot {index}:**"
                    )

                    for key, value in result.items():

                        if value is None:
                            continue

                        formatted_key = (
                            str(key)
                            .replace("_", " ")
                            .title()
                        )

                        lines.append(
                            f"• **{formatted_key}:** {value}"
                        )

                    lines.append("")

                result_text = "\n".join(lines)

                # Discord message limit
                if len(result_text) > 1900:

                    result_text = (
                        result_text[:1890]
                        + "\n..."
                    )

                await self._edit_message(
                    loading_message,
                    result_text
                )

        except Exception as exc:

            print(
                "[SSVERIFY] Unexpected error: "
                f"{type(exc).__name__}: {exc}"
            )

            await self._edit_message(
                loading_message,
                (
                    "❌ **SS Verification failed.**\n"
                    "Please try again later."
                )
            )


async def setup(bot):
    await bot.add_cog(
        Ssverification(bot)
    )
