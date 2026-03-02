export default function RecentActivity() {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-2">Activité récente</h2>
      <ul className="text-sm text-gray-700 space-y-1">
        <li>📚 Nouvel étudiant ajouté</li>
        <li>🗓️ Cours de math mis à jour</li>
        <li>👨‍🏫 Nouveau professeur inscrit</li>
      </ul>
    </div>
  );
}
