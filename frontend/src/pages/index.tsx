import { Button } from '../components/atoms/Button';

export default function Home() {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Welcome to Real Estate Platform</h1>
      <Button variant="primary">Click Me</Button>
      <Button variant="secondary">Secondary Button</Button>
    </div>
  );
}