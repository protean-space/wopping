import React, { useRef, useEffect } from "react";
import ForceGraph3D from "3d-force-graph";
import SpriteText from "three-spritetext";

const Graph3D: React.FC = () => {
  const graphRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (graphRef.current) {
      const Graph = ForceGraph3D();
      const graph = Graph(graphRef.current);

      // グラフのデータ
      graph.graphData({
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
      graph.linkWidth((link: any) => link.value || 1.8);
      graph.linkColor(() => "#FFFFFF");

      // ノードを文字列に設定
      graph.nodeThreeObject((node: any) => {
        const text = new SpriteText(node.id);
        text.color = "#00ff00";
        text.textHeight = 6;
        return text;
      });

      // ウィンドウがリサイズされたとき用のリスナー
      window.addEventListener("resize", () => {
        graph.width(window.innerWidth);
        graph.height(window.innerHeight);
      });

      // 初期サイズ設定
      graph.width(window.innerWidth);
      graph.height(window.innerHeight);
    }

    return () => {
      window.removeEventListener("resize", () => {
        if (graphRef.current) {
          const graph = ForceGraph3D()(graphRef.current);
          graph.width(window.innerWidth);
          graph.height(window.innerHeight);
        }
      });
    };
  }, []);

  return <div ref={graphRef} style={{ width: "100%", height: "100%" }} />;
};

export default Graph3D;
