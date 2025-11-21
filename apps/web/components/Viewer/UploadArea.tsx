"use client";

import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";

export default function UploadArea() {
  const t = useTranslations("upload"); //i18n

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadResult, setUploadResult] = useState<"success" | "error" | null>(
    null
  ); // 文件上传状态
  const [showNotification, setShowNotification] = useState(false); // 控制通知显示

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
    event.preventDefault(); // 必须阻止默认行为，以便触发 drop
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
      setError(t("invalid_type"));
      setShowNotification(true);
      setUploadResult("error");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError(t("invalid_size"));
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

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error();
      }

      setUploading(false);
      setSelectedFile(null);
      setUploadResult("success");
      setShowNotification(true);
      console.log("Upload successful");
    } catch (err: any) {
      setError(err.message || t("upload_failed"));
      setUploading(false);
      setUploadResult("error");
      setShowNotification(true);
      console.log("Upload f");
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
              ? t("upload_successed")
              : error != null
              ? error
              : t("upload_failed")}
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
          <p className="text-lg font-medium text-gray-800 mb-1">{t("tips")}</p>

          {/* button text */}
          <button
            type="button"
            className="inline-flex rounded-full px-8 py-2 font-medium cursor-pointer
                       bg-sky-500 hover:bg-sky-600 text-white shadow transition mt-8"
          >
            {t("button")}
          </button>

          <input
            ref={inputRef}
            type="file"
            accept="application"
            multiple
            className="hidden"
            onChange={handleChange}
          />
        </div>
      </div>
    </div>
  );
}
