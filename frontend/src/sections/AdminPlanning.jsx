import React from "react";
import Card from "../components/Card";
import Badge from "../components/Badge";

const AdminPlanning = () => (
  <section id="admin" className="section">
    <div className="section__header">
      <div>
        <p className="eyebrow">Admin-Planung</p>
        <h2>Dienstplanung & Ressourcen</h2>
        <p className="subtitle">
          Verteile Dienste, plane Vertretungen und behalte die Auslastung der Teams im Blick.
        </p>
      </div>
    </div>

    <div className="grid grid--3">
      <Card title="Offene Dienste" action={<Badge tone="warning">5 offen</Badge>}>
        <p>Plane weitere Messdiener*innen für kommende Gottesdienste ein.</p>
        <ul className="list">
          <li>So, 10:00 Uhr – Hochamt</li>
          <li>Mi, 18:00 Uhr – Abendmesse</li>
          <li>Sa, 19:00 Uhr – Jugendmesse</li>
        </ul>
      </Card>
      <Card title="Backup-Pool" action={<Badge tone="success">8 verfügbar</Badge>}>
        <p>Der Pool ist gut gefüllt. Spare Ressourcen für kurzfristige Ausfälle.</p>
        <button type="button" className="button button--secondary">Backup-Kandidaten prüfen</button>
      </Card>
      <Card title="Benachrichtigungen" action={<Badge tone="accent">12 gesendet</Badge>}>
        <p>Aktive Hinweise an Teamleitungen und Eltern für spontane Vertretungen.</p>
        <button type="button" className="button">Neue Nachricht</button>
      </Card>
    </div>
  </section>
);

export default AdminPlanning;
