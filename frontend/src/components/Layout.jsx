import React from "react";
import Navigation from "./Navigation";

const Layout = ({ children }) => (
  <div className="layout">
    <Navigation />
    <main>{children}</main>
    <footer className="footer">
      <p>MesseCall · Dienstplanung & Austausch für Messdiener*innen</p>
      <a href="#dashboard">Nach oben</a>
    </footer>
  </div>
);

export default Layout;
