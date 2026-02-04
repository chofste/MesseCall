import React from "react";
import Card from "../components/Card";
import Badge from "../components/Badge";

const Landing = ({ upcomingEvents, highlights }) => (
  <section id="dashboard" className="section">
    <div className="section__header">
      <div>
        <p className="eyebrow">Willkommen zurück</p>
        <h1>Dein Dashboard für die Messdiener*innen-Planung</h1>
        <p className="subtitle">
          Behalte anstehende Dienste, offene Anfragen und deine Verdienste im Blick.
        </p>
      </div>
      <div className="hero-card">
        <p className="hero-card__title">Nächster Dienst</p>
        <h2>{upcomingEvents[0]?.title ?? "Keine öffentlichen Termine"}</h2>
        <p>{upcomingEvents[0]?.time ?? "Bitte neue Planung starten"}</p>
        <Badge tone="accent">In 3 Tagen</Badge>
      </div>
    </div>

    <div className="grid grid--3">
      {highlights.map((item) => (
        <Card key={item.title} title={item.title} action={<Badge tone={item.tone}>{item.badge}</Badge>}>
          <p>{item.description}</p>
        </Card>
      ))}
    </div>
  </section>
);

export default Landing;
