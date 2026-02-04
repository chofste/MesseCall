import React from "react";
import Card from "../components/Card";
import Badge from "../components/Badge";

const Gamification = () => (
  <section id="gamification" className="section">
    <div className="section__header">
      <div>
        <p className="eyebrow">Gamification</p>
        <h2>Fortschritt & Belohnungen</h2>
        <p className="subtitle">Motivation durch Level, Badges und Punkte für Ersatzdienste.</p>
      </div>
    </div>

    <div className="grid grid--3">
      <Card title="Punkte-Stand" action={<Badge tone="success">420 Punkte</Badge>}>
        <p>Du stehst kurz vor dem nächsten Level!</p>
        <div className="progress">
          <div className="progress__bar" style={{ width: "72%" }} />
        </div>
        <p className="muted">Level 4 · 80 Punkte bis Level 5</p>
      </Card>
      <Card title="Badges" action={<Badge tone="accent">3 aktiv</Badge>}>
        <ul className="badge-list">
          <li><Badge tone="success">Retter</Badge></li>
          <li><Badge tone="warning">Wochenendprofi</Badge></li>
          <li><Badge tone="neutral">Teamplayer</Badge></li>
        </ul>
      </Card>
      <Card title="Top-Leistungen" action={<Badge tone="neutral">Leaderboard</Badge>}>
        <ol className="list list--ordered">
          <li>Anna Schmitt – 420 Punkte</li>
          <li>Leon König – 390 Punkte</li>
          <li>Mia Hoffmann – 355 Punkte</li>
        </ol>
      </Card>
    </div>
  </section>
);

export default Gamification;
