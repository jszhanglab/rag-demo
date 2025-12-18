// apps/web/app/[locale]/page.tsx
import Sidebar from "@/components/Sidebar/Sidebar";
import Viewer from "@/components/Viewer/Viewer";
import ChatPanel from "@/components/ChatPanel/ChatPanel";

type PageProps = {
  searchParams: Promise<{
    doc?: string;
    page?: string;
    thread?: string;
  }>;
};

export default async function Page(
  /**
   * 'searchParams' is a Next.js built-in property that automatically
   * contains the URL query parameters of the current request.
   * You must name it 'searchParams'. Next.js only recognizes this name.
   *
   * searchParams は、ページにアクセスしたときに Next.js が自動で
   * URL のクエリパラメーターを渡してくれる特別な props です。
   * 'searchParams'と命名しなければならない。Next.js はこの名前だけを認識します。
   */
  { searchParams }: PageProps
) {
  const sp = await searchParams;
  const docId = sp?.doc ?? null;
  const page = Number(sp?.page ?? 1) || 1;
  const threadId = sp?.thread ?? null;

  // The 3 columns themselves are laid out by <main> in [locale]/layout.tsx.
  // We just render the three sections in order.
  return (
    <>
      <section className="overflow-y-auto bg-slate-50">
        <Sidebar />
      </section>

      <section className="overflow-y-auto bg-white">
        <Viewer docId={docId} page={page} />
      </section>

      <section className="overflow-y-auto bg-white">
        <ChatPanel docId={docId} threadId={threadId} />
      </section>
    </>
  );
}
