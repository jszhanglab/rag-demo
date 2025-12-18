// apps/web/i18n/request.ts
import {
  getRequestConfig,
  type GetRequestConfigParams,
} from "next-intl/server";

export default getRequestConfig(async ({ locale }: GetRequestConfigParams) => {
  const current = locale ?? "en";
  return {
    locale: current,
    messages: (await import(`./messages/${current}.json`)).default,
  };
});
