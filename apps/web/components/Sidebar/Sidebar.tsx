"use client";
export default function Sidebar() {
  return (
    <div className="p-4 text-sm space-y-2">
      <div className="font-semibold">📄 Mock Sidebar</div>
      <ul className="space-y-1">
        <li className="hover:bg-muted px-2 py-1 rounded cursor-pointer">
          document_1.pdf
        </li>
        <li className="hover:bg-muted px-2 py-1 rounded cursor-pointer">
          contract_A.pdf
        </li>
        <li className="hover:bg-muted px-2 py-1 rounded cursor-pointer">
          invoice_2025.pdf
        </li>
      </ul>
    </div>
  );
}
