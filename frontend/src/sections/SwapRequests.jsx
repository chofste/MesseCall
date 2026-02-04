import React, { useState } from "react";
import Card from "../components/Card";
import Badge from "../components/Badge";
import { createSwapRequest } from "../api";

const SwapRequests = () => {
  const [assignmentId, setAssignmentId] = useState(1);
  const [requestedUsers, setRequestedUsers] = useState("2,3");
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setStatus(null);
    try {
      const payload = {
        assignment_id: Number(assignmentId),
        requested_user_ids: requestedUsers
          .split(",")
          .map((value) => Number(value.trim()))
          .filter((value) => !Number.isNaN(value))
      };
      const response = await createSwapRequest(payload);
      setStatus({ type: "success", message: `Anfrage #${response.id} erstellt.` });
    } catch (error) {
      setStatus({ type: "error", message: "Anfrage konnte nicht erstellt werden." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="swap" className="section">
      <div className="section__header">
        <div>
          <p className="eyebrow">Tausch & Ersatz</p>
          <h2>Ersatzdienst anfragen</h2>
          <p className="subtitle">Schnell Ersatz finden – direkt verbunden mit /swap-requests.</p>
        </div>
      </div>

      <div className="grid grid--2">
        <Card title="Neue Tauschanfrage" action={<Badge tone="warning">Benötigt Ersatz</Badge>}>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Assignment-ID
              <input
                type="number"
                min="1"
                value={assignmentId}
                onChange={(event) => setAssignmentId(event.target.value)}
                required
              />
            </label>
            <label>
              Gewünschte User-IDs (kommagetrennt)
              <input
                type="text"
                value={requestedUsers}
                onChange={(event) => setRequestedUsers(event.target.value)}
                required
              />
            </label>
            <button className="button" type="submit" disabled={loading}>
              {loading ? "Sende ..." : "Anfrage senden"}
            </button>
          </form>
          {status && (
            <p className={`status status--${status.type}`}>{status.message}</p>
          )}
        </Card>
        <Card title="Offene Anfragen" action={<Badge tone="accent">3 offen</Badge>}>
          <ul className="list">
            <li>
              <strong>So, 10:00 Uhr</strong> – Ersatz für Hochamt
              <span className="muted">· 2 Zusagen offen</span>
            </li>
            <li>
              <strong>Mi, 18:00 Uhr</strong> – Jugendmesse
              <span className="muted">· Anfrage läuft</span>
            </li>
            <li>
              <strong>Sa, 19:00 Uhr</strong> – Abendmesse
              <span className="muted">· Rückmeldung erwartet</span>
            </li>
          </ul>
        </Card>
      </div>
    </section>
  );
};

export default SwapRequests;
