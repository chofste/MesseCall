import React from "react";
import Card from "../components/Card";
import Badge from "../components/Badge";

const ProfilePreferences = () => (
  <section id="profile" className="section">
    <div className="section__header">
      <div>
        <p className="eyebrow">Profil & Präferenzen</p>
        <h2>Messdiener*innen-Profil</h2>
        <p className="subtitle">Verwalte Verfügbarkeiten, Wunschdienste und Benachrichtigungen.</p>
      </div>
    </div>

    <div className="grid grid--2">
      <Card title="Persönliche Daten" action={<Badge tone="neutral">Aktiv</Badge>}>
        <div className="stack">
          <div>
            <p className="muted">Name</p>
            <strong>Anna Schmitt</strong>
          </div>
          <div>
            <p className="muted">Rolle</p>
            <strong>Messdienerin · Team Süd</strong>
          </div>
          <div>
            <p className="muted">Kontakt</p>
            <strong>anna.schmitt@example.com</strong>
          </div>
        </div>
      </Card>
      <Card title="Präferenzen & Verfügbarkeit" action={<Badge tone="accent">Top Match</Badge>}>
        <ul className="list">
          <li>Bevorzugte Tage: Samstag, Sonntag</li>
          <li>Vermeiden: Schulferien</li>
          <li>Benachrichtigungen: Push & E-Mail</li>
        </ul>
        <button className="button button--secondary" type="button">Präferenzen bearbeiten</button>
      </Card>
    </div>
  </section>
);

export default ProfilePreferences;
