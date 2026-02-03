import { ThemeToggle } from '../shared/ThemeToggle'

interface HeaderProps {
  title: string
  subtitle: string
  badge?: string
}

export function Header({ title, subtitle, badge }: HeaderProps) {
  return (
    <header className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
      <div className="flex flex-col gap-1">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">OpenOA</p>
        <h1 className="text-3xl font-semibold text-slate-900 dark:text-slate-100">{title}</h1>
        <p className="text-sm text-slate-600 dark:text-slate-400">{subtitle}</p>
      </div>
      <div className="flex items-center gap-3">
        <ThemeToggle />
        {badge ? (
          <span className="inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300">
            {badge}
          </span>
        ) : null}
      </div>
    </header>
  )
}
