import React, { useRef, useEffect } from "react";
import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";

const Graph3D: React.FC = () => {
  const graphRef = useRef<HTMLDivElement>(null);
  const graph = useRef<any>(null); // `any`型を使用

  useEffect(() => {
    if (graphRef.current) {
      graph.current = ForceGraph3D()(graphRef.current);

      // グラフのデータ
      graph.current.graphData({
        nodes: [
          { id: "スポーツ施設" },
          { id: "サッカー" },
          { id: "介護保険" },
          { id: "人口" },
          { id: "年齢" },
          { id: "施設費用" },
          { id: "ボランティア" },
          { id: "目黒区" },
          { id: "介護施設" },
        ],
        links: [
          { source: "スポーツ施設", target: "サッカー" },
          { source: "スポーツ施設", target: "年齢" },
          { source: "スポーツ施設", target: "施設費用" },
          { source: "スポーツ施設", target: "目黒区" },
          { source: "年齢", target: "人口" },
          { source: "介護保険", target: "施設費用" },
          { source: "介護施設", target: "施設費用" },
          { source: "施設費用", target: "目黒区" },
          { source: "サッカー", target: "ボランティア" },
          { source: "ボランティア", target: "年齢" },
        ],
      });

      // リンクのカスタマイズ
      if (graph.current) {
        graph.current.linkWidth((link: any) => link.value || 1.8);
        graph.current.linkColor(() => "#FFFFFF");
      }

      // ノードを文字列に設定
      graph.current.nodeThreeObject((node: any) => {
        const text = new SpriteText(node.id);
        text.color = "#00ff00";
        text.textHeight = 6;
        return text;
      });
    }

    return () => {
      graph.current = null;
    };
  }, []);

  return <div ref={graphRef} style={{ width: "100%", height: "100vh" }} />;
};

export default Graph3D;
