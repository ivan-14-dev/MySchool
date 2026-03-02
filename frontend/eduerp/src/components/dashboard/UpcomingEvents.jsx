export default function UpcomingEvents() {
  const events = [
    { date: "12 Oct 2025", title: "Réunion du corps enseignant" },
    { date: "14 Oct 2025", title: "Examen de mi-semestre" },
    { date: "20 Oct 2025", title: "Conférence des étudiants" },
  ];

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-3">Événements à venir</h2>
      <ul className="space-y-2 text-sm text-gray-700">
        {events.map((event, index) => (
          <li
            key={index}
            className="flex justify-between items-center border-b pb-1"
          >
            <span>{event.title}</span>
            <span className="text-gray-500 text-xs">{event.date}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
