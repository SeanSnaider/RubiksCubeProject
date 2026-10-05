/**
 * Tests for solve-time formatting.
 */
import { describe, expect, it } from 'vitest'
import { formatTime } from './formatTime'

describe('formatTime', () => {
    it('shows times under ten seconds without a leading zero', () => {
        expect(formatTime(5230)).toBe('5.23')
        expect(formatTime(0)).toBe('0.00')
    })

    it('shows times under a minute as seconds', () => {
        expect(formatTime(12_345)).toBe('12.34')
    })

    it('truncates rather than rounds, so 59.999s never shows as 60.00', () => {
        expect(formatTime(59_999)).toBe('59.99')
    })

    it('shows minutes with zero-padded seconds', () => {
        expect(formatTime(65_430)).toBe('1:05.43')
        expect(formatTime(600_000)).toBe('10:00.00')
    })

    it('shows DNF for an infinite time', () => {
        expect(formatTime(Infinity)).toBe('DNF')
    })
})
