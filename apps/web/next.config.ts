/**
 * next.config.ts is the main configuration file for a Next.js project.
 * It tells Next.js how to build, run, and optimize your app.
 *   -Environment variables (env)
 *   -Image optimization (images)
 *   -Internationalization (i18n)
 *   -Webpack / Turbopack behavior
 *   -API route handling
 *   -Plugins (like next-intl/plugin)
 */

import createNextIntlPlugin from "next-intl/plugin";

const withNextIntl = createNextIntlPlugin("./i18n/request.ts");

const nextConfig = {};
export default withNextIntl(nextConfig);
