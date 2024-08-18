import React, { useState } from "react";
import TagInput from "@pathofdev/react-tag-input";
import "@pathofdev/react-tag-input/build/index.css";

const TagForm: React.FC = () => {
  const [tags, setTags] = useState<string[]>([]);
  const maxTags = 3; // 3つの単語まで

  // バリデーション
  const handleTagChange = (newTags: string[]) => {
    if (newTags.length <= maxTags) {
      setTags(newTags);
    } else {
      alert(`${maxTags}つの単語までしか入力することができません！`);
    }
  };

  // 検索処理
  const handleSearch = () => {
    if (tags.length > 0) {
      // 検索(post)処理の実装部分。
      alert(`Searching for: ${tags.join(", ")}`);
    } else {
      alert("単語を入力してください。");
    }
  };

  return (
    <div style={{ maxWidth: "700px", margin: "0 auto", padding: "20px" }}>
      <h3>文献 - 単語検索</h3>
      <div style={{ display: "flex", alignItems: "center" }}>
        <TagInput
          tags={tags}
          onChange={handleTagChange}
          placeholder="単語を入力してください"
        />
        <button
          onClick={handleSearch}
          style={{
            marginLeft: "8px",
            padding: "8px 8px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </div>
      <p
        style={{ fontSize: "10px", color: "yellow" }}
      >{`${maxTags}つの単語まで入力できます`}</p>
    </div>
  );
};

export default TagForm;
