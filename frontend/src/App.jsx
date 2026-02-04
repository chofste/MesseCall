import React, { useEffect, useState } from "react";
import Layout from "./components/Layout";
import Landing from "./sections/Landing";
import EventListing from "./sections/EventListing";
import AdminPlanning from "./sections/AdminPlanning";
import ProfilePreferences from "./sections/ProfilePreferences";
import SwapRequests from "./sections/SwapRequests";
import Gamification from "./sections/Gamification";
import { fetchEvents, fetchPublicEvents } from "./api";

const highlightCards = [
  {
    title: "Offene Tauschanfragen",
    description: "3 Anfragen warten auf Bestätigung im Team.",
    badge: "3 offen",
    tone: "warning"
  },
  {
    title: "Bestätigte Dienste",
    description: "Du bist für 4 Dienste im nächsten Monat eingeteilt.",
    badge: "4 geplant",
    tone: "success"
  },
  {
    title: "Gamification",
    description: "Sammle Punkte für jeden Ersatzdienst.",
    badge: "Level 4",
    tone: "accent"
  }
];

const App = () => {
  const [events, setEvents] = useState([]);
  const [publicEvents, setPublicEvents] = useState([]);
  const [churchId, setChurchId] = useState("1");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadEvents = async () => {
      setLoading(true);
      try {
        const response = await fetchEvents();
        setEvents(response);
      } catch (error) {
        setEvents([]);
      } finally {
        setLoading(false);
      }
    };

    loadEvents();
  }, []);

  useEffect(() => {
    const loadPublicEvents = async () => {
      if (!churchId) {
        return;
      }
      try {
        const response = await fetchPublicEvents(churchId);
        setPublicEvents(response);
      } catch (error) {
        setPublicEvents([]);
      }
    };

    loadPublicEvents();
  }, [churchId]);

  const upcomingEvents = events.map((event) => ({
    title: event.title,
    time: new Date(event.start_time).toLocaleString("de-DE", {
      weekday: "short",
      hour: "2-digit",
      minute: "2-digit"
    })
  }));

  return (
    <Layout>
      <Landing upcomingEvents={upcomingEvents} highlights={highlightCards} />
      <EventListing
        events={events}
        publicEvents={publicEvents}
        churchId={churchId}
        onChurchIdChange={setChurchId}
        loading={loading}
      />
      <AdminPlanning />
      <ProfilePreferences />
      <SwapRequests />
      <Gamification />
    </Layout>
  );
};

export default App;
