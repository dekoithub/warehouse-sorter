CREATE TABLE destinations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT destinations_code_positive
        CHECK (code > 0)
);

CREATE TABLE items (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    barcode TEXT NOT NULL UNIQUE,
    weight NUMERIC(10, 3) NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    length INTEGER NOT NULL,
    category TEXT NOT NULL,
    delivery_type TEXT NOT NULL,
    is_flammable BOOLEAN NOT NULL DEFAULT FALSE,
    status TEXT NOT NULL,
    destination_id BIGINT,
    location TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT items_weight_positive
        CHECK (weight > 0),

    CONSTRAINT items_dimensions_positive
        CHECK (
            width > 0
            AND height > 0
            AND length > 0
        ),

    CONSTRAINT items_status_valid
        CHECK (
            status IN (
                'CREATED',
                'SCANNING',
                'ROUTING',
                'MOVING',
                'BUFFERED',
                'SORTED',
                'MANUAL_PROCESSING',
                'ERROR'
            )
        ),

    CONSTRAINT items_destination_fk
        FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE SET NULL
);

CREATE TABLE routes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    barcode TEXT NOT NULL UNIQUE,
    destination_id BIGINT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOT(),

    CONSTRAINT routes_destination_fk
        FOREIGN KEY (destination_id)
        REFERENCES destinations(id)
        ON DELETE RESTRICT
);