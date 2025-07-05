import { API_BASE } from "./api";

export async function classifyDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/classify/`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Failed to classify document");

  return await res.json(); // { document_type, confidence, text }
}

export async function submitFeedback(
  text: string,
  predicted_label: string,
  correct_label: string
) {
  const res = await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    body: new URLSearchParams({
      text,
      predicted_label,
      correct_label,
    }),
  });

  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || "Feedback submission failed.");
  }

  return { message: "Thanks for your feedback!" };
}