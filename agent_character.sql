/*
 Navicat Premium Dump SQL

 Source Server         : buddy_backend
 Source Server Type    : PostgreSQL
 Source Server Version : 160001 (160001)
 Source Host           : 172.31.64.2:5432
 Source Catalog        : buddy_backend
 Source Schema         : buddy

 Target Server Type    : PostgreSQL
 Target Server Version : 160001 (160001)
 File Encoding         : 65001

 Date: 01/09/2025 14:18:30
*/


-- ----------------------------
-- Table structure for agent_character
-- ----------------------------
DROP TABLE IF EXISTS "buddy"."agent_character";
CREATE TABLE "buddy"."agent_character" (
  "id" int4 NOT NULL DEFAULT nextval('"buddy".agent_character_seq'::regclass),
  "name" varchar COLLATE "pg_catalog"."default",
  "prompt" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for agent_chat
-- ----------------------------
DROP TABLE IF EXISTS "buddy"."agent_chat";
CREATE TABLE "buddy"."agent_chat" (
  "id" int4 NOT NULL DEFAULT nextval('"buddy".agent_chat_id_seq'::regclass),
  "user_id" int4 NOT NULL,
  "chat_content" json NOT NULL,
  "character" varchar COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS "buddy"."alembic_version";
CREATE TABLE "buddy"."alembic_version" (
  "version_num" varchar(32) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS "buddy"."transactions";
CREATE TABLE "buddy"."transactions" (
  "id" int4 NOT NULL DEFAULT nextval('"buddy".transactions_id_seq'::regclass),
  "amount" float8 NOT NULL,
  "remark" varchar COLLATE "pg_catalog"."default",
  "user_id" int4 NOT NULL,
  "timestamp" timestamp(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "buddy"."users";
CREATE TABLE "buddy"."users" (
  "id" int4 NOT NULL DEFAULT nextval('"buddy".users_id_seq'::regclass),
  "account" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "hashed_password" varchar COLLATE "pg_catalog"."default" NOT NULL,
  "is_active" bool,
  "limit" json
)
;

-- ----------------------------
-- Indexes structure for table agent_character
-- ----------------------------
CREATE INDEX "ix_buddy_agent_character_id" ON "buddy"."agent_character" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table agent_character
-- ----------------------------
ALTER TABLE "buddy"."agent_character" ADD CONSTRAINT "agent_character_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table agent_chat
-- ----------------------------
CREATE INDEX "ix_buddy_agent_chat_id" ON "buddy"."agent_chat" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table agent_chat
-- ----------------------------
ALTER TABLE "buddy"."agent_chat" ADD CONSTRAINT "agent_chat_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table alembic_version
-- ----------------------------
ALTER TABLE "buddy"."alembic_version" ADD CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num");

-- ----------------------------
-- Indexes structure for table transactions
-- ----------------------------
CREATE INDEX "ix_buddy_transactions_id" ON "buddy"."transactions" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table transactions
-- ----------------------------
ALTER TABLE "buddy"."transactions" ADD CONSTRAINT "transactions_amount_key" UNIQUE ("amount");

-- ----------------------------
-- Primary Key structure for table transactions
-- ----------------------------
ALTER TABLE "buddy"."transactions" ADD CONSTRAINT "transactions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table users
-- ----------------------------
CREATE INDEX "ix_buddy_users_id" ON "buddy"."users" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table users
-- ----------------------------
ALTER TABLE "buddy"."users" ADD CONSTRAINT "users_account_key" UNIQUE ("account");

-- ----------------------------
-- Primary Key structure for table users
-- ----------------------------
ALTER TABLE "buddy"."users" ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");
