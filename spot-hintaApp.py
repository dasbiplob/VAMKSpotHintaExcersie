import asyncio

from datetime import date
from spothinta import SpotHinta


async def main() -> None:
    """Show example on fetching the energy prices from spot-hinta.fi."""
    async with SpotHinta() as client:
        energy = await client.energy_prices()


if __name__ == "__main__":
    asyncio.run(main())
