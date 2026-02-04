import React from "react";

const Table = ({ caption, columns, rows }) => (
  <div className="table-wrapper">
    <table>
      <caption>{caption}</caption>
      <thead>
        <tr>
          {columns.map((column) => (
            <th key={column}>{column}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.id || row.label}>
            {row.cells.map((cell, index) => (
              <td key={`${row.id}-${index}`}>{cell}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default Table;
