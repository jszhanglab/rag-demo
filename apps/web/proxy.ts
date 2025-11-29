/**
 * --- 2025/11/23 change this file's name to proxy.ts as middleware has been deprecated since Next.js 16 ---
 * middleware.ts is a built-in feature of Next.js that runs before any route or page.
 * It’s used for authentication, i18n, redirects, logging, etc.
 * The matcher defines which paths it applies to.
 * It’s called “middleware” because it sits in the middle between the incoming request and your route handlers — not a dispatcher.
 */

/**
 * proxy.ts acts as a request proxy, forwarding incoming requests to backend services or APIs,
 * while handling logic like dynamic routing, API request forwarding, and cross-origin resource sharing (CORS).
 *
 * It helps centralize request management for handling things like authentication, language redirection,
 * and more, without exposing backend service details directly to the frontend.
 */

import { NextRequest, NextResponse } from "next/server";
import createIntlMiddleware from "next-intl/middleware";
import { locales, defaultLocale } from "./i18n/i18n";

//  next-intl handle function
const handleI18nRouting = createIntlMiddleware({
  locales,
  defaultLocale,
  localeDetection: true, // Automatically detect the user's browser language ONLY when the URL does not include a locale (e.g. visiting "/").
});

export default async function middleware(request: NextRequest) {
  const url = request.nextUrl;
  const isApiRequest = url.pathname.startsWith("/api");

  // Api request should not use i18n
  if (isApiRequest) {
    const API_BASE_URL = "http://127.0.0.1:8000";

    // remove '/api'
    const targetPath = url.pathname.replace("/api", "");

    const targetUrl = new URL(targetPath, API_BASE_URL);
    //get all the search parameters
    url.searchParams.forEach((value, key) => {
      targetUrl.searchParams.set(key, value);
    });

    const requestHeaders = new Headers(request.headers);
    requestHeaders.set("x-forwarded-host", request.headers.get("host") || "");

    const response = NextResponse.rewrite(targetUrl, {
      request: {
        headers: requestHeaders,
      },
    });

    // set CORS response headers
    // response.headers.set('Access-Control-Allow-Origin', '*');

    return response;
  }

  // Not Api reques should use i18n
  const response = handleI18nRouting(request);

  return response;
}

//matcher
export const config = {
  matcher: ["/((?!_next|.*\\..*).*)"],
};
