import React from "react";
import Card from "../components/Card";
import Table from "../components/Table";

const EventListing = ({ events, publicEvents, churchId, onChurchIdChange, loading }) => {
  const tableRows = (events.length ? events : []).map((event) => ({
    id: event.id,
    cells: [event.title, event.start_time, event.location ?? "Kirche", event.is_public ? "Öffentlich" : "Intern"]
  }));

  const publicRows = (publicEvents.length ? publicEvents : []).map((event) => ({
    id: `public-${event.id}`,
    cells: [event.title, event.start_time, event.location ?? "Kirche", event.is_public ? "Öffentlich" : "Intern"]
  }));

  return (
    <section id="events" className="section">
      <div className="section__header">
        <div>
          <p className="eyebrow">Öffentliche Termine</p>
          <h2>Event-Listing</h2>
          <p className="subtitle">Direkte API-Integration für öffentliche und interne Events.</p>
        </div>
        <div className="input-group">
          <label htmlFor="churchId">Kirchen-ID</label>
          <input
            id="churchId"
            type="number"
            min="1"
            value={churchId}
            onChange={(event) => onChurchIdChange(event.target.value)}
          />
        </div>
      </div>

      <div className="grid grid--2">
        <Card
          title="Alle Events"
          action={<span className="muted">{loading ? "Lädt ..." : `${events.length} Einträge`}</span>}
        >
          <Table
            caption="Interne Eventliste"
            columns={["Titel", "Start", "Ort", "Sichtbarkeit"]}
            rows={tableRows.length ? tableRows : [{
              id: "placeholder",
              cells: ["Keine Daten", "-", "-", "-"]
            }]}
          />
        </Card>
        <Card
          title="Öffentliche Events"
          action={<span className="muted">{publicEvents.length} Einträge</span>}
        >
          <Table
            caption="Öffentliche Events der Gemeinde"
            columns={["Titel", "Start", "Ort", "Sichtbarkeit"]}
            rows={publicRows.length ? publicRows : [{
              id: "placeholder-public",
              cells: ["Keine öffentlichen Events", "-", "-", "-"]
            }]}
          />
        </Card>
      </div>
    </section>
  );
};

export default EventListing;
