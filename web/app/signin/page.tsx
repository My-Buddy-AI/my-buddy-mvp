import React from 'react'
import cn from 'classnames'
import Script from 'next/script'
import Forms from './forms'
import Header from './_header'
import style from './page.module.css'
import { IS_CE_EDITION } from '@/config'

const SignIn = () => {
  return (
    <>
      {!IS_CE_EDITION && (
        <>
          {/* <Script strategy="beforeInteractive" async src={'https://www.googletagmanager.com/gtag/js?id=AW-11217955271'}></Script> */}
          <Script
            id="ga-monitor-register"
            dangerouslySetInnerHTML={{
              __html: `
window.dataLayer2 = window.dataLayer2 || [];
function gtag(){dataLayer2.push(arguments);}
gtag('js', new Date());
gtag('config', 'AW-11217955271"');
        `,
            }}
          ></Script>
        </>
      )}
      <div
        className={cn(
          style.background,
          'flex w-full min-h-screen',
          'justify-center lg:justify-start',
        )}
      >
        <div
          className={cn(
            style.wrapper,
            'lg:flex w-full lg:w-1/2 login_img_section justify-around items-center',
          )}
        >
        </div>
        <div
          className={cn(
            style.bgWrapper,
            'flex-col flex w-full lg:w-1/2 bg-white shadow shrink-0',
            'space-between',
          )}
        >
          <Header />
          <Forms />
          <div className="px-8 py-6 text-sm text-center font-normal text-gray-500">
            © {new Date().getFullYear()} My-Buddy.AI, Ltd. All rights reserved.
          </div>
        </div>
      </div>
    </>
  )
}

export default SignIn
