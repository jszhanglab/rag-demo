//middleware.ts is a built-in feature of Next.js that runs before any route or page.
//It’s used for authentication, i18n, redirects, logging, etc.
//The matcher defines which paths it applies to.
//It’s called “middleware” because it sits in the middle between the incoming request and your route handlers — not a dispatcher.

import createMiddleware from "next-intl/middleware";
import { locales, defaultLocale } from "./i18n/i18n";

/**
 * This is function from next-intl library
 */
export default createMiddleware({
  locales,
  defaultLocale,
  localeDetection: true, // Automatically detect the user's browser language ONLY when the URL does not include a locale (e.g. visiting "/").
});

export const config = {
  matcher: ["/((?!_next|.*\\..*|api).*)"],
};
