import React from "react";

const Card = ({ title, children, action }) => (
  <section className="card" aria-label={title}>
    <header className="card__header">
      <h3>{title}</h3>
      {action}
    </header>
    <div className="card__body">{children}</div>
  </section>
);

export default Card;
