import React, { useState } from "react";
import axios from "axios";

const ImagePoemChatbot = () => {
  const [image, setImage] = useState(null);
  const [poem, setPoem] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setImage(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post("http://localhost:5000/generate_poem", formData);
      setPoem(response.data.text);
    } catch (error) {
      console.error("Error generating poem:", error);
      setPoem("Failed to generate poem. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4">Image Poem Generator</h1>
      <input type="file" accept="image/*" onChange={handleImageUpload} className="mb-4 choose-file" /><br/>
      {image && <img height={200} width={200} src={image} alt="Uploaded Preview" className="w-64 h-auto mb-4 rounded-lg image-uploaded" />}
      {loading ? (
            <p className="text-lg font-semibold text-indigo-600 animate-pulse">✨ Generating poem...</p>
        ) : (
            <p className="text-lg font-medium text-gray-700">{poem || "Your poem will appear here!"}</p>
      )}
    </div>
  );
};

export default ImagePoemChatbot;
