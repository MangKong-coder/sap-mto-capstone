# ──────────────
# 1. Build Stage
# ──────────────
FROM oven/bun:1 AS builder

WORKDIR /app

# Copy dependency files first for caching
COPY bun.lock package.json ./

# Install dependencies (production + dev)
RUN bun install

# Copy the rest of the source code
COPY . .

# Build the Next.js app
RUN bun run build

# ──────────────
# 2. Run Stage
# ──────────────
FROM oven/bun:1 AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3000

# Copy only what's needed for runtime
COPY --from=builder /app/package.json ./
COPY --from=builder /app/bun.lock ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.ts ./next.config.ts

# Expose port 3000 for Next.js
EXPOSE 3000

# Run the Next.js server
CMD ["bun", "run", "start"]
