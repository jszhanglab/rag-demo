// apps/web/app/[locale]/page.tsx
import WorkspaceClient from "@/components/Workspace/WorkspaceClient";

type PageProps = {
  searchParams: Promise<{
    doc?: string;
    page?: string;
    thread?: string;
  }>;
};

export default async function Page({ searchParams }: PageProps) {
  const sp = await searchParams;

  return <WorkspaceClient />;
}
