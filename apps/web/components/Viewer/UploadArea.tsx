// apps\web\components\Viewer\UploadArea.tsx
"use client";

import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { API_ROUTES } from "@/constants/apiRoutes";
import { mutate } from "swr";

export default function UploadArea() {
  const i18n = useTranslations("upload"); //i18n

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadResult, setUploadResult] = useState<"success" | "error" | null>(
    null
  );
  const [showNotification, setShowNotification] = useState(false);

  const inputRef = useRef<HTMLInputElement>(null);

  const handleClick = () => {
    if (inputRef.current) {
      inputRef.current.click();
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileValidation(file);
    }
  };

  const handleDragOver = (event: React.DragEvent) => {
    event.preventDefault();
  };

  const handleDrop = (event: React.DragEvent) => {
    event.preventDefault();
    event.stopPropagation();

    const file = event.dataTransfer.files?.[0];
    if (file) {
      handleFileValidation(file);
    }
  };

  const handleFileValidation = (file: File) => {
    if (file.type !== "application/pdf") {
      setError(i18n("invalid_type"));
      setShowNotification(true);
      setUploadResult("error");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError(i18n("invalid_size"));
      setShowNotification(true);
      setUploadResult("error");
      return;
    }
    setSelectedFile(file);
    setError(null);
    handleUpload(file);
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    setError(null);

    //clear upload file name to make sure same file can re-upload until refresh page
    if (inputRef.current) {
      inputRef.current.value = "";
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(API_ROUTES.UPLOAD_DOCUMENT, {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(i18n("upload_failed"));
      }

      /**
       * `mutate` works as a cache-based synchronization mechanism in SWR.
       * By invalidating the cache for `API_ROUTES.GET_FILE_LIST`, it forces
       * all components using this key to refetch the data, which effectively
       * keeps different parts of the UI in sync without direct component communication.
       */
      await mutate(API_ROUTES.GET_FILE_LIST);

      setUploading(false);
      setSelectedFile(null);
      setUploadResult("success");
      setShowNotification(true);
      // Reset the file input's value.
      // This is necessary because the browser suppresses the 'onChange' event
      // if the user selects the exact same file path again without a page refresh.
      if (inputRef.current) {
        inputRef.current.value = "";
      }
    } catch (err) {
      setUploading(false);
      setUploadResult("error");
      setShowNotification(true);
      const errorMessage =
        err instanceof Error && err.message !== ""
          ? err.message
          : i18n("upload_failed");
      setError(errorMessage);

      if (inputRef.current) {
        inputRef.current.value = "";
      }
    }
  };

  useEffect(() => {
    if (showNotification) {
      const timer = setTimeout(() => {
        setShowNotification(false);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [showNotification]);

  return (
    <div className="w-full flex items-center justify-center">
      <div className="w-[720px] rounded-3xl border border-purple-200 bg-white/70 shadow-sm px-8 py-10 ">
        {showNotification && (
          <div
            className={`${
              uploadResult === "success"
                ? "bg-green-100 text-green-800"
                : uploadResult === "error"
                ? "bg-red-100 text-red-800"
                : ""
            } p-3 rounded-lg fixed top-10 left-1/2 transform -translate-x-1/2 transition-opacity opacity-100`}
          >
            {uploadResult === "success"
              ? i18n("upload_successed")
              : error != null
              ? error
              : i18n("upload_failed")}
          </div>
        )}
        <div
          className={`
            hover:bg-sky-50 relative flex flex-col items-center justify-center 
            rounded-2xl border-2 border-dashed px-10 py-12 cursor-pointer transition
            `}
          onClick={handleClick}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-white shadow">
            <span className="text-3xl">📄</span>
          </div>

          {/* tips */}
          <p className="text-lg font-medium text-gray-800 mb-1">
            {i18n("tips")}
          </p>

          {/* button text */}
          <button
            disabled={uploading}
            type="button"
            className={`
                inline-flex rounded-full px-8 py-2 font-medium 
                shadow transition mt-8 
             ${
               uploading
                 ? "bg-gray-400 cursor-not-allowed"
                 : "bg-sky-500 hover:bg-sky-600 cursor-pointer text-white"
             }
           `}
          >
            {uploading ? i18n("uploading") : i18n("button")}
          </button>

          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            multiple
            className="hidden"
            onChange={handleChange}
          />
        </div>
      </div>
    </div>
  );
}
