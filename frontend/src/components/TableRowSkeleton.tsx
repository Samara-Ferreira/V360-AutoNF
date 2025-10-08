export function TableRowSkeleton() {
  return (
    <tr className="border-b border-gray-200">
      <td className="p-4">
        <div className="flex items-center gap-3">
          <div className="h-5 w-5 bg-gray-200 rounded-full animate-pulse"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse"></div>
        </div>
      </td>

      <td className="p-4 text-right">
        <div className="h-10 w-28 bg-gray-200 rounded-lg animate-pulse ml-auto"></div>
      </td>
    </tr>
  );
}
