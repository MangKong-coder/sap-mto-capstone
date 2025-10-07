import { z } from "zod"

export const ApiResponseSchema = <T extends z.ZodType>(dataSchema: T) =>
    z.object({
      success: z.literal(true),
      data: dataSchema,
      message: z.string().nullable().optional()
    })


/**
 * Zod schema for API Error response wrapper
 */
export const ApiErrorResponseSchema = z.object({
  success: z.literal(false),
  error: z.string(),
  message: z.string()
})
