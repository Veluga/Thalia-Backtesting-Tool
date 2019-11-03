BEGIN;
--
-- Alter field abbreviation on asset
--
CREATE TABLE "new__MVG_asset" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "abbreviation" varchar(255) NOT NULL UNIQUE, "name" varchar(255) NOT NULL, "asset_class_id" integer NOT NULL REFERENCES "MVG_assetclass" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__MVG_asset" ("id", "name", "asset_class_id", "abbreviation") SELECT "id", "name", "asset_class_id", "abbreviation" FROM "MVG_asset";
DROP TABLE "MVG_asset";
ALTER TABLE "new__MVG_asset" RENAME TO "MVG_asset";
CREATE INDEX "MVG_asset_asset_class_id_4a5cb1ef" ON "MVG_asset" ("asset_class_id");
--
-- Alter field name on asset
--
CREATE TABLE "new__MVG_asset" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "abbreviation" varchar(255) NOT NULL UNIQUE, "asset_class_id" integer NOT NULL REFERENCES "MVG_assetclass" ("id") DEFERRABLE INITIALLY DEFERRED, "name" varchar(255) NOT NULL UNIQUE);
INSERT INTO "new__MVG_asset" ("id", "abbreviation", "asset_class_id", "name") SELECT "id", "abbreviation", "asset_class_id", "name" FROM "MVG_asset";
DROP TABLE "MVG_asset";
ALTER TABLE "new__MVG_asset" RENAME TO "MVG_asset";
CREATE INDEX "MVG_asset_asset_class_id_4a5cb1ef" ON "MVG_asset" ("asset_class_id");
--
-- Alter field name on assetclass
--
CREATE TABLE "new__MVG_assetclass" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(255) NOT NULL UNIQUE);
INSERT INTO "new__MVG_assetclass" ("id", "name") SELECT "id", "name" FROM "MVG_assetclass";
DROP TABLE "MVG_assetclass";
ALTER TABLE "new__MVG_assetclass" RENAME TO "MVG_assetclass";
COMMIT;
