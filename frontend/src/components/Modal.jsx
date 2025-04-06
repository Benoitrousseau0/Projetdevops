export default function Modal({ children }) {
  return (
    <div className="fixed inset-0 flex justify-center items-center bg-black/60 backdrop-blur-sm z-50">
      <div className="bg-gray-900 border border-white/10 p-6 rounded-2xl shadow-xl w-full max-w-md animate-fade-in">
        {children}
      </div>
    </div>
  );
}
