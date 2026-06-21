from utils.database import (
    get_connection
)


def signal_exists(
    symbol,
    side,
    zone_start,
    zone_end
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM signals
        WHERE symbol=?
        AND side=?
        AND zone_start=?
        AND zone_end=?
        LIMIT 1
        """,
        (
            symbol,
            side,
            zone_start,
            zone_end
        )
    )

    row = cursor.fetchone()

    conn.close()

    return row is not None


def add_signal(
    symbol,
    side,
    zone_start,
    zone_end
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO signals
        (
            symbol,
            side,
            zone_start,
            zone_end
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            symbol,
            side,
            zone_start,
            zone_end
        )
    )

    conn.commit()

    conn.close()
