import { NextIntlClientProvider } from "next-intl";
import { locales, Locale } from "@/i18n/i18n";
import "../globals.css";
import Shell from "@/components/Shell/Shell";

/**
 * layout
 *   └─ Shell
 *        └─ page
 *             └─ Hider(i18n)
 *             └─ Sidebar / Viewer / ChatPanel
 */

/**
 * This function is a Next.js special export for dymatic routes.
 * It runs at build time and tells Next.js which parameters(locales in this case)
 * should be statically generated.
 * Each returned object corresponds to a route like /en, /ja or /zh
 * @returns 
 * [  { locale: 'en' },
      { locale: 'ja' },
      { locale: 'zh' }
    ]
 */
export function generateStaticParams() {
  return locales.map((locale) => ({ locale })); // locales.map((locale) => { return { locale: locale };});
}

/**
 * Nest.js built-in metadata genarate function.
 * @param params
 * @returns metadata
 */
export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: Locale }>;
}) {
  const { locale } = await params;

  try {
    const messages = (await import(`@/i18n/messages/${locale}.json`)).default;

    return {
      title: messages.meta?.title ?? "RAG Demo",
      description: messages.meta?.description ?? "RAG Demo",
    };
  } catch (e) {
    return {
      title: "RAG Demo",
    };
  }
}

export default async function RootLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: Locale }>;
}) {
  const { locale } = await params;

  const messages = (await import(`@/i18n/messages/${locale}.json`)).default;

  return (
    <html lang={locale}>
      <body>
        <NextIntlClientProvider locale={locale} messages={messages}>
          <Shell locale={locale}>{children}</Shell>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
