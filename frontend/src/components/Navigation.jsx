import React from "react";

const navItems = [
  { href: "#dashboard", label: "Dashboard" },
  { href: "#events", label: "Events" },
  { href: "#admin", label: "Admin-Planung" },
  { href: "#profile", label: "Profil" },
  { href: "#swap", label: "Tausch/Ersatz" },
  { href: "#gamification", label: "Gamification" }
];

const Navigation = () => (
  <nav className="nav" aria-label="Hauptnavigation">
    <a className="nav__logo" href="#dashboard">MesseCall</a>
    <ul>
      {navItems.map((item) => (
        <li key={item.href}>
          <a href={item.href}>{item.label}</a>
        </li>
      ))}
    </ul>
    <button className="nav__cta" type="button">Neue Anfrage</button>
  </nav>
);

export default Navigation;
