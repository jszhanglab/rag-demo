import { API_ROUTES } from "./apiRoutes";

export const buildDocumentDetailUrl = (documentId: string) => {
  return API_ROUTES.GET_DOCUMENT_DETAIL.replace(
    "{document_id}",
    encodeURIComponent(documentId),
  );
};
